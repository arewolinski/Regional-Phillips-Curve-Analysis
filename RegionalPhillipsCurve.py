import pandas as pd
import numpy as np
import streamlit as st




# Need the absolute paths to the csv files because the current working directory is fucking with me for some reason
#These are going to be global variables so I can access them at all times
df_cpi = pd.read_csv('/Users/alexrewolinski/Desktop/Phillips Curve Project/Regional Phillips Curve/Code/Core CPI by Region.csv')
df_unem = pd.read_csv('/Users/alexrewolinski/Desktop/Phillips Curve Project/Regional Phillips Curve/Code/Unemployment Rate by Region.csv')


def create_inflation(df_cpi):
    """
    This function will take my core cpi data and output an inflation data frame with date in one column and inflation by region
    (measured as percent change in core CPI from the previous year) in the other 4 columns

    Inputs: df_cpi - A data frame object from the pandas library

    Output: A data frame from the pandas library with the dates in one column and the inflation by region in the other 4 columns
    """

    date_column = df_cpi['Time Period'].iloc[12:450]
    df_inflation = pd.DataFrame({
        "Dates": date_column, 
        "Midwest Region": None, 
        "Northeast Region": None, 
        "South Region": None, 
        "West Region": None})
    

    for row in range(12, 450):

        for col in range(1, 5):

            df_inflation.iloc[row - 12, col] = ((df_cpi.iloc[row, col] - df_cpi.iloc[row - 12, col]) / df_cpi.iloc[row - 12, col]) * 100


    return df_inflation




print(create_inflation(df_cpi))







