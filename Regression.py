import pandas as pd
import numpy as np
import RegionalPhillipsCurve as rpc
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression as lm


def main_function(time_period, type_of_regression, type_of_fit, leverage):
    """
    This function coordinates all of the other functions within this script and relies on them heavily to output the final result. This function is not long because it uses helper functions
    to do the majority of the nitty-gritty work. In the end, the basic structure of this function is calling the function that cleans the data to the specifications of the user, calling the 
    function that performs linear regression on the data, and then outputting a mapping from region to a list of figure and R2 and coefficients.

    Inputs:

    time_period - A list of two elements where the first element is a String of the start date and the second element is a String of the end date (the Streamlit class will check the validity
    of these dates so we don't have to check that on the back-end here)

    type_of_regression - A string that is either "1-lag" or "2-lag" that specifies the type of regression that the user wants to perform

    type_of_fit - A string that is either "linear" or "exponential" that specifies the type of fit that the user wants to perform

    leverage - A string that is either "Leave leverage points in dataset" or "Omit leverage points from dataset" that specifies how the leverage points should be handled

    Outputs:
    A list of two elements:

    1) A dictionary that maps a region to a list of figures, R2 values, and coefficients.

    2) A dictionary that maps a region to a list of dates that were removed from the dataset since they were leverage points.
    """

    prepped_data, removed_leverage_points = clean_data(time_period, type_of_regression, type_of_fit, leverage)


    output_mapping = {}

    for region in prepped_data.keys():
        x_data = prepped_data[region][0]
        y_data = prepped_data[region][1]

        current_list = regression(x_data, y_data, time_period, type_of_regression, type_of_fit, region)
        output_mapping[region] = current_list
    
    return output_mapping, removed_leverage_points



def clean_data(time_period, type_of_regression, type_of_fit, leverage):
    """
    This function takes in the time period, type of regression, and type of fit and returns a mapping of the region to a list of 2 elements where the first element is a numpy array that represents
    the x data that has been cleaned and the second element is a numpy array that represents the y data that has been cleaned (x data is 2 dimensional and y data is 1 dimensional). Note that since the 
    x data is 2 dimensional, depending on the amount of lags requested by the user, there could be multiple different 1-D arrays within this numpy array object.

    Inputs:

    time_period - A list of two elements where the first element is a String of the start date and the second element is a String of the end date (the Streamlit class will check the validity
    of these dates so we don't have to check that on the back-end here)

    type_of_regression - A string that is either "1-lag" or "2-lag" that specifies the type of regression that the user wants to perform

    type_of_fit - A string that is either "linear" or "exponential" that specifies the type of fit that the user wants to perform

    leverage - A string that is either "Leave leverage points in dataset" or "Omit leverage points from dataset" that specifies how the leverage points should be handled

    Outputs:

    A mapping from the US Census Bureau geographic region to a list of 2 elements where the first element is a numpy array that represents the x data that has been cleaned 
    and the second element is a numpy array that represents the y data that has been cleaned.
    """

    unem_data, infl_data = create_data(time_period, type_of_regression)

    regional_data = matrix_to_mapping(unem_data, infl_data)

    removed_indices = []
    if leverage == "Omit leverage points from dataset":
        regional_data, removed_indices = remove_leverage_points(regional_data)


    # Initialize a dictionary to hold the cleaned data by region
    data_by_region = {}

    # Loop through each region
    for region in regional_data.keys(): 
        #We are grabbing the unemployment array from the mapping for the current region and turning it into a 2-D array so that it can be dealt with
        x_data = regional_data[region][0][region].values.reshape(-1,1) #First indexing into the dictionary to get the list, then indexing into the list to get the first element, then indexing into the pandas dataframe to get the array

        # Align y_data (inflation) with the lagged x_data (y_data is ok as a 1-D array)
        y_data = regional_data[region][1][region].reset_index(drop=True) #First indexing into the dictionary to get the list, then indexing into the list to get the first element, then indexing into the pandas dataframe to get the array, then slicing the array

        # Log-transform the y_data if an exponential fit is requested
        if type_of_fit == "Log transform y array":
            y_data = np.log(y_data.astype(np.float64))

        # Store the cleaned x_data and y_data in the dictionary
        data_by_region[region] = [x_data, y_data]

    return data_by_region, removed_indices


def regression(x_data, y_data, time_period, type_of_regression, type_of_fit, region):
    """
    This function takes in the x data and y data and performs linear regression on the data. It returns a list of 3 elements where the first element is a matplotlib object that represents the figure,
    the second element is a float that represents the R^2 value of the model, and the third element is a list that represents the coefficients of the model.

    Inputs:

    x_data - A numpy array that represents the x data that has been cleaned (2 dimensional)

    y_data - A numpy array that represents the y data that has been cleaned (1 dimensional)

    Outputs:

    A list of 3 elements where the first element is a matplotlib object that represents the figure, the second element is a float that represents the R^2 value of the model, and 
    the third element is a list that represents the coefficients of the model.
    """
    # Initialize the Linear Regression model and fit it to the data
    model = lm().fit(x_data, y_data)

    # Calculate the R^2 value
    r_sq = model.score(x_data, y_data)

    # Retrieve the coefficients
    intercept = model.intercept_
    coefficients = model.coef_

    # Generate points for plotting the regression line
    x_line = np.linspace(x_data.min(), x_data.max(), 100).reshape(-1, x_data.shape[1])
    y_line = model.predict(x_line)

    # Plot the scatter plot and regression line
    fig, ax = plt.subplots()
    ax.scatter(x_data[:, 0], y_data, label='Data Points')
    ax.plot(x_line[:, 0], y_line, color='red', label='Regression Line')

    # Title and labels (Assuming region information is available)
    if type_of_fit == "Log transform y array":
        title = f'{type_of_regression} Regression from {time_period[0]} to {time_period[1]} with Log-Transformed Y data for {region}'
    else:
        title = f'{type_of_regression} Regression from {time_period[0]} to {time_period[1]} for {region}'

    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Unemployment (%)', fontweight='bold')
    ax.set_ylabel('Inflation (yearly % change Core CPI)', fontweight='bold')
    ax.legend()

    # Return the figure, R^2 value, and coefficients
    return [fig, r_sq, intercept.tolist(), coefficients.tolist()]

#HELPER FUNCTION FOR CLEAN_DATA
def create_data(time_period, type_of_regression):
    """
    This function takes in a time period and a type of regression and is going to output the unemployment matrices and inflation matrices for those time periods. Remember that this function is called
    before matrix_to_mapping is called so we are dealing with matrices here.

    Inputs:
    time_period - A list of two elements where the first element is a String of the start date and the second element is a String of the end date (the Streamlit class will check the validity
    of these dates so we don't have to check that on the back-end here)

    type_of_regression - A string that is either "No lag", "1-lag", "2-lags", "3-lags", or "4-lags" that specifies the type of regression that the user wants to perform

    Outputs:
    A tuple of two elements:

    1) A pandas dataframe with 5 columns where the cells represent unemployment data: 1) time period, 2) Midwest Region, 3) Northeast Region, 4) South Region, 5) West Region

    2) A pandas dataframe with 5 columns where the cells represent inflation data: 1) time period, 2) Midwest Region, 3) Northeast Region, 4) South Region, 5) West Region
    """
    # Fetching the datasets
    unem_data = rpc.get_unem()
    infl_data = rpc.create_inflation()

    # Convert the 'Dates' columns to datetime objects
    unem_data['Time Period'] = pd.to_datetime(unem_data['Time Period'])
    infl_data['Time Period'] = pd.to_datetime(infl_data['Time Period'])

    # Parse time period
    start_date = pd.to_datetime(time_period[0])
    end_date = pd.to_datetime(time_period[1])

    # Determine the number of lags based on type_of_regression
    if type_of_regression == "No lag":
        lag = 0
    elif type_of_regression == "1-lag":
        lag = 1
    elif type_of_regression == "2-lags":
        lag = 2
    elif type_of_regression == "3-lags":
        lag = 3
    elif type_of_regression == "4-lags":
        lag = 4

    # Adjust the start date to account for lags
    adjusted_start_date = start_date - pd.DateOffset(months=lag)
    adjusted_end_date = end_date - pd.DateOffset(months=lag)

    # Filter the data based on the adjusted start date and end date
    unem_data = unem_data[(unem_data['Time Period'] >= adjusted_start_date) & (unem_data['Time Period'] <= adjusted_end_date)].reset_index(drop=True)
    infl_data = infl_data[(infl_data['Time Period'] >= start_date) & (infl_data['Time Period'] <= end_date)].reset_index(drop=True)

    return unem_data, infl_data

#HELPER FUNCTION FOR CLEAN_DATA
def remove_leverage_points(regional_data):
    """
    Removes leverage points from the datasets based on the unemployment data (independent variable).
    
    Inputs:
    regional_data - A mapping where the keys are the US Census Bureau regions in a String and the values are a list of two elements where the first element is a pandas dataframe with 2 columns
    where the first column is the time period and the second column is the unemployment data and the second element is a pandas dataframe with 2 columns where the first column is the time period
    and the second column is the inflation data.

    Outputs:
    A list with two elements:

    1) A mapping where the keys are the US Census Bureau regions in a String and the values are a list of two elements where the first element is a pandas dataframe with 2 columns
    where the first column is the time period and the second column is the unemployment data and the second element is a pandas dataframe with 2 columns where the first column is the time period
    and the second column is the inflation data. However, the leverage points for each US Census Bureau region have been removed.

    2) A mapping where the keys are the US Census Bureau regions in a String and the values are a list of the dates removed from the dataset since they were leverage points
    """

    output_data_mapping = {}
    output_indices_mapping = {}

    # Assume the first column is the 'Time Period', so we start from the second column
    for region in regional_data.keys():  

        # Calculate leverage points using standardized residuals for unemployment data
        current_unem_data = regional_data[region][0][region]
        current_infl_data = regional_data[region][1][region]

        threshold = 4 / len(current_unem_data)  # Set the threshold for leverage points at 4 / n

        mean = np.mean(current_unem_data)

        Sxx = 0
        # Using this for loop to calculate Sxx
        for stat in current_unem_data:
            Sxx += ((stat - mean) ** 2)
        
        # Calculate standardized residuals
        hii = (1 / len(current_unem_data)) + (((current_unem_data - mean) ** 2) / Sxx)

        # Identify indices of leverage points
        leverage_indices = hii > threshold

        #Storing the unemployment data as a dataframe where the first column is the time period and the second column is the unemployment data
        current_unem_dataframe = pd.DataFrame({'Time Period': regional_data[region][0]['Time Period'][~leverage_indices], region: current_unem_data[~leverage_indices]}).reset_index(drop=True)
        current_infl_dataframe = pd.DataFrame({'Time Period': regional_data[region][1]['Time Period'][~leverage_indices], region: current_infl_data[~leverage_indices]}).reset_index(drop=True)
                    
        #Putting the unemployment dataframe and the inflation dataframe in our list
        current_data_value = [current_unem_dataframe, current_infl_dataframe]
        current_indices_value = regional_data[region][0]['Time Period'][leverage_indices].tolist() #Taking the leverage_indices variable from earlier and using it to select the YYYY-MM_DD that have been removed

        # current_indices_value - [dt.strftime('%Y-%m-%d') for dt in current_indices_value] #Converting the datetime objects to strings so they print out nice

        #Store the cleaned data and the indices
        output_data_mapping[region] = current_data_value 
        output_indices_mapping[region] = current_indices_value 
    

    return output_data_mapping, output_indices_mapping


#HELPER FUNCTION FOR CLEAN_DATA
def matrix_to_mapping(unem_data, infl_data):
    """
    This function is going to take our two matrices (which is a matrix for the unemployment data and a matrix for the inflation data) and output a mapping where the keys are the regions
    in a String and the values are a list of two elements where the first element is the unemployment data and the second element is the inflation data. This matrix_to_mapping allows us
    to tailor our removal of leverage points to each region rather than requiring the same amount of leverage points be removed from each region. If we were to keep our data in matrix form and 
    get rid of a different number of leverage points for each region then we would no longer have a matrix and the code would throw an error.

    Inputs:

    unem_data - A pandas dataframe with 5 columns where the cells represent unemployment data: 1) time period, 2) Midwest Region, 3) Northeast Region, 4) South Region, 5) West Region
    infl_data - A pandas dataframe with 5 columns where the cells represent inflation data: 1) time period, 2) Midwest Region, 3) Northeast Region, 4) South Region, 5) West Region

    Output:

    A mapping where the keys are a String of the US Census Bureau region and the values are a list of two elements where the first element is the unemployment data and the second element is the 
    inflation data.
    """

    output_mapping = {}

    date_array = unem_data["Time Period"] # Storing the time period array in the date_array variable outside the for loop so that we can insert this within every pandas dataframe as the first column

    for region in unem_data.columns[1:]:

        current_pandas_unem = pd.DataFrame({'Time Period': date_array, region: unem_data[region]})
        current_pandas_infl = pd.DataFrame({'Time Period': date_array, region: infl_data[region]})

        output_mapping[region] = [current_pandas_unem, current_pandas_infl]


    return output_mapping



#SOMETHING IS GETTING FUCKED UP WITH THE LAG AND THE MATRIX_TO_MAPPING FUNCTION (TAKE A LOOK AT THE PRINTED DATAFRAMES AND GO FROM THERE)
# print(clean_data(["2020-01-01", "2024-01-01"], "2-lags", "Linear", "Omit leverage points from dataset"))

#Looking at the Midwest here
# output_mapping = main_function(["2000-01-01", "2020-01-01"], "No lag", "Linear")['Midwest Region'][0]
# print(output_mapping['Midwest Region'][0])
# plt.show()



