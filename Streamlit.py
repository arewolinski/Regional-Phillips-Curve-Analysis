import streamlit as st
import pandas as pd
import RegionalPhillipsCurve as rpc
import DataVisualizations as dv
import Regression as rg


def main():
    """
    Main function that is run when Streamlit is run from the command line. It delegates to other helper functions throughout for better
    modularity.
    """

    st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90%;
        padding-left: 10%;
        padding-right: 10%;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )


    # Create tabs
    tabs = st.tabs(["Visualizing Unemployment & Inflation", "Phillips Curve Analysis"])

    with tabs[0]:
        tab_one()
    
    with tabs[1]:
        tab_two()


def tab_one():
    """
    This function populates the first tab that the user can click. It's functionality is that the user can select a date and unemployment or
    inflation and they can see a spatial heatmap of unemployment or inflation (whatever they selected) by US Census Bureau Region for that
    particular date.
    """

    st.title("Unemployment and Inflation by US Census Bureau Region")
    st.write("""
    # Overview

    Before looking at the Phillips Curve relationship, let's first look at **unemployment** and **inflation** data by US Census Bureau region.

    The US Census Bureau divides the US into 4 regions: 
    - **Midwest**
    - **Northeast**
    - **South**
    - **West**

    The Bureau of Economic Analysis provides core CPI data by US Census Bureau region, which we use to calculate inflation. The Federal Reserve Economic Data (FRED) provides unemployment data by US Census Bureau region.
    """)

    date_list = rpc.create_inflation()['Time Period'].values
    selected_date = st.selectbox('Choose a date:', date_list)

    selected_visualization = st.selectbox('Choose a visualization:', ['Unemployment', 'Inflation'])

    if st.button('Submit', key='tab 1'):
        # Call function based on data_type
        if selected_visualization == 'Unemployment':
        
            st.pyplot(dv.output_spatial_unemployment(selected_date))
        
        elif selected_visualization == 'Inflation':
        
            st.pyplot(dv.output_spatial_inflation(selected_date))
        
        else:
            st.write('Error. Somehow you selected neither unemployment nor inflation. Please try again.')

def tab_two():
    """
    This tab looks at the Phillips Curve relationship between unemployment and inflation. It allows the user to select a start date
    and an end date. When the user presses submit, 4 regression plots pop up (one for each region), showing the relationship between
    unemployment and inflation as well as some summary statistics such as R^2. 
    """


    st.title("Phillips Curve Analysis")

    st.write("""
    # Overview

    The Phillips Curve postulates that there is an inverse relationship between unemployment and inflation. In other words, when
             unemployment decreases, there is pressure on inflation to increase and vice versa. The general chain of logic is as follows:
    
    - **Logic for unemployment decrease and inflation increase:** Unemployment decreases; real wages increase (since there is more competition between firms for workers); consumers have more money to spend; consumer demand
             increases; firms increase prices in response to this demand; inflation increases.
    
    - **Logic for unemployment increase and inflation decrease:** Unemployment increases; real wages decrease (since there is more competition between workers for firms); consumers have less money to spend; consumer demand
             decreases; firms decrease prices in response to this demand; inflation decreases.
             
    The Phillips Curve was seen as an ironclad law in the 1950s and 1960s, but it has since fallen out of favor due to the stagflation of the 1970s and the 
             seeming flattness of the curve today. Recent flattening highlights the fickle nature of the Phillips Curve logic and how changes in firms behaviors (which could keep prices high even though demand has come down) or changes in consumer behavior (which is often irrational) can prevent the Phillips Curve
             from having its expected behavior.
    
    We will look at the Phillips Curve relationship between unemployment and inflation by US Census Bureau region. Adjust the specifications of the model in order to see
             if you can find the best fit relationship!
    
    # Model:
    """)


    date_list = rpc.create_inflation()['Time Period'].values
    start_date = st.selectbox('Choose a start date:', date_list)
    end_date = st.selectbox('Choose an ends date:', date_list)

    selected_lag = st.selectbox('Choose a type of regression:', ['No lag', '1-lag', '2-lags', '3-lags', '4-lags'])

    selected_model = st.selectbox('Choose a transformation:', ['No Transformation', 'Log transform y array'])

    selected_leverage = st.selectbox('How do you want to deal with leverage points?:', ['Leave leverage points in dataset', 'Omit leverage points from dataset'])

    if st.button('Submit', key='tab 2'):

        #Need to check that the end date falls after the start date
        check_start = pd.to_datetime(start_date)
        check_end = pd.to_datetime(end_date)

        # Calculate the date that is one year after check_start
        one_year_later = check_start + pd.DateOffset(years=1)

        if check_end < one_year_later:
            st.write(":red[ERROR:] The end date must be at least one year after the start date.")
            return

        # Output mapping's values are a list with 4 elements: 1) fig, 2) r2, 3) intercept, 4) coefficient (3 and 4 are packaged in a list)
        output_mapping, indices_removed_mapping = rg.main_function([start_date, end_date], selected_lag, selected_model, selected_leverage)

        figures = []
        r2_values = []
        intercepts = []
        slopes = []

        for region in output_mapping.keys():
            figures.append(output_mapping[region][0])
            r2_values.append(output_mapping[region][1])
            intercepts.append(output_mapping[region][2])
            slopes.append(output_mapping[region][3][0])

        # Create a 2x2 grid layout
        col1, col2 = st.columns([2,2])

        # Display the first row of plots
        with col1:
            st.pyplot(figures[0])
            st.markdown(f"**R²:** {r2_values[0]:.2f}")
            st.markdown(f"**Intercept:** {intercepts[0]:.2f}")
            st.markdown(f"**Slope:** {slopes[0]:.2f}")

            #We only want to display the leverage points removed if the user selected to omit leverage points from the dataset
            if(selected_leverage == 'Omit leverage points from dataset'):
                #Have to do special formatting for my leverage points
                midwest_header = "Leveraged Indices Removed"
                midwest_markdown_list = "\n".join([f"- {item}" for item in indices_removed_mapping['Midwest Region']])
                st.markdown(f"**{midwest_header}**\n\n{midwest_markdown_list}")

        with col2:
            st.pyplot(figures[1])
            st.markdown(f"**R²:** {r2_values[1]:.2f}")
            st.markdown(f"**Intercept:** {intercepts[1]:.2f}")
            st.markdown(f"**Slope:** {slopes[1]:.2f}")
            
            #We only want to display the leverage points removed if the user selected to omit leverage points from the dataset
            if(selected_leverage == 'Omit leverage points from dataset'):
                #Have to do special formatting for my leverage points
                northeast_header = "Leveraged Indices Removed"
                northeast_markdown_list = "\n".join([f"- {item}" for item in indices_removed_mapping['Northeast Region']])
                st.markdown(f"**{northeast_header}**\n\n{northeast_markdown_list}")

        # Create a second row of plots
        col3, col4 = st.columns([2,2])

        with col3:
            st.pyplot(figures[2])
            st.markdown(f"**R²:** {r2_values[2]:.2f}")
            st.markdown(f"**Intercept:** {intercepts[2]:.2f}")
            st.markdown(f"**Slope:** {slopes[2]:.2f}")
            
            #We only want to display the leverage points removed if the user selected to omit leverage points from the dataset
            if(selected_leverage == 'Omit leverage points from dataset'):
                #Have to do special formatting for my leverage points
                south_header = "Leveraged Indices Removed"
                south_markdown_list = "\n".join([f"- {item}" for item in indices_removed_mapping['South Region']])
                st.markdown(f"**{south_header}**\n\n{south_markdown_list}")

        with col4:
            st.pyplot(figures[3])
            st.markdown(f"**R²:** {r2_values[3]:.2f}")
            st.markdown(f"**Intercept:** {intercepts[3]:.2f}")
            st.markdown(f"**Slope:** {slopes[3]:.2f}")
            
            #We only want to display the leverage points removed if the user selected to omit leverage points from the dataset
            if(selected_leverage == 'Omit leverage points from dataset'):
                #Have to do special formatting for my leverage points
                west_header = "Leveraged Indices Removed"
                west_markdown_list = "\n".join([f"- {item}" for item in indices_removed_mapping['West Region']])
                st.markdown(f"**{west_header}**\n\n{west_markdown_list}")



if __name__ == '__main__':
    main()

# st.pyplot(dv.output_spatial_inflation('2004-06-01'))



