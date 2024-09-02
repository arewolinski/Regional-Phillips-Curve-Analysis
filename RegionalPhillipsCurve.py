import pandas as pd

# Need the absolute paths to the csv files because the current working directory is fucking with me for some reason
#These are going to be global variables so I can access them at all times

def get_cpi():
    """
    Using a getter function for the CPI data which is good coding practice to not have global variables.
    """

    return pd.read_csv('/Users/alexrewolinski/Desktop/Phillips Curve Project/Regional Phillips Curve/Code/Core CPI by Region.csv')

def get_unem():
    """
    Using a getter function for the Unemployment data which is good coding practice to not have global variables.

    """

    return pd.read_csv('/Users/alexrewolinski/Desktop/Phillips Curve Project/Regional Phillips Curve/Code/Unemployment Rate by Region.csv')
    



def create_inflation():
    """
    This function will take my core cpi data and output an inflation data frame with date in one column and inflation by region
    (measured as percent change in core CPI from the previous year) in the other 4 columns

    Inputs: df_cpi - A data frame object from the pandas library

    Output: A data frame from the pandas library with the dates in one column and the inflation by region in the other 4 columns
    """

    date_column = get_cpi()['Time Period'].iloc[12:450]

    df_inflation = pd.DataFrame({
        "Time Period": date_column, 
        "Midwest Region": None, 
        "Northeast Region": None, 
        "South Region": None, 
        "West Region": None})
    

    for row in range(12, 450):

        for col in range(1, 5):

            #Doing a percent change from the year prior and rounding to two digits
            df_inflation.iloc[row - 12, col] = round(((get_cpi().iloc[row, col] - get_cpi().iloc[row - 12, col]) / get_cpi().iloc[row - 12, col]) * 100, 2)

    #Resetting the index so that the first row has index 0 (this way we won't get incorrect numbers when we index into the data frame)
    return df_inflation.reset_index(drop = True)


def output_regional_unemployment(date):
    """
    This function takes in a valid date (between 1987-01-01 and 2024-06-01) and outputs the regional unemployment rates by region
    for that year. They are output in alphabetical order, so Midwest, Northeast, South, West.

    Inputs: date - a string representing a year in yyyy-mm-01 format

    Ouputs: A list with 4 elements representing the regional unemployment rates for the given date. They are output in alphabetical order.
    """

    #Checking the bounds of the years
    if date not in get_unem()['Time Period'].values:
        return "Invalid date. Please enter a date between 1987-01-01 and the present in yyyy-mm-01 format."

    #Finding the index of the year in the data frame
    index = get_unem()[get_unem()['Time Period'] == date].index[0]

    #Returning a list using the index we previously found
    return [get_unem().iloc[index, 1], get_unem().iloc[index, 2], get_unem().iloc[index, 3], get_unem().iloc[index, 4]]


def output_regional_inflation(date):
    """
    This function takes in a valid date (which is between 1988-01-01 and 2024-06-01) and outputs the regional unemployment rates 
    by region for that year. They are output in alphabetical order, so Midwest, Northeast, South, West.

    Inputs: date - a string representing a year in yyyy-mm-01 format

    Ouputs: A list with 4 elements representing the regional inflation rates for the given date. They are output in alphabetical order.
    """
    #Getting my inflation data frame from the function
    inflation = create_inflation()

    # #Checking if it is a valid date
    if date not in inflation['Time Period'].values:
        return "Invalid date. Please enter a date between 1988-01-01 and the present in yyyy-mm-01 format."

    #Finding the index of the year in the data frame   
    index = inflation[inflation['Time Period'] == date].index[0]

    #Returning a list using the index we previously found
    return [inflation.iloc[index, 1], inflation.iloc[index, 2], inflation.iloc[index, 3], inflation.iloc[index, 4]]





