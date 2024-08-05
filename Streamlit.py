import streamlit as st
import RegionalPhillipsCurve as rpc
import DataVisualizations as dv


# def main():
#     """
#     Main function that is run when Streamlit is run from the command line. It delegates to other helper functions throughout for better
#     modularity.
#     """


# def tab_one():
#     """
#     This function populates the first tab that the user can click. It's functionality is that the user can select a date and unemployment or
#     inflation and they can see a spatial heatmap of unemployment or inflation (whatever they selected) by US Census Bureau Region for that
#     particular date.
#     """

#     st.title("Unemployment and Inflation by US Census Bureau Region")
#     st.write("""
#     # Overview

#     Before looking at the Phillips Curve relationship, let's first look at **unemployment** and **inflation** data by US Census Bureau region.

#     The US Census Bureau divides the US into 4 regions: 
#     - **Midwest**
#     - **Northeast**
#     - **South**
#     - **West**

#     The Bureau of Economic Analysis provides core CPI data by US Census Bureau region, which we use to calculate inflation. The Federal Reserve Economic Data (FRED) provides unemployment data by US Census Bureau region.
#     """)

#     date_list = rpc.create_inflation()['Dates'].values
#     selected_date = st.selectbox('Choose a date:', date_list)

#     selected_visualization = st.selectbox('Choose a visualization:', ['Unemployment', 'Inflation'])

#     if st.button('Submit'):
#         # Call function based on data_type
#         if selected_visualization == 'Unemployment':
        
#             st.pyplot(dv.output_spatial_unemployment())
        
#         elif selected_visualization == 'Inflation':
        
#             "Don't have this function quite yet. Give me a second."
        
#         else:
#             st.write('Error. Somehow you neither selected unemployment nor inflation. Please try again.')





# if __name__ == '__main__':
#     main()

st.pyplot(dv.output_spatial_inflation('2004-06-01'))



