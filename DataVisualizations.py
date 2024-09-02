import geopandas as gpd
import matplotlib.pyplot as plt
import RegionalPhillipsCurve as rpc



def output_spatial_unemployment(date):
    """
    This function creates a spatial plot of the unemployment rate for a given date. It uses the RegionalPhillipsCurve module to get 
    the unemployment rate for each region in the US and puts it on a heatmap using geopandas and matplotlib.

    Inputs: date - a string in the format 'YYYY-MM-DD'

    Outputs: A matplotlib plot of the unemployment rate for each region in the US.
    """

    #Getting the shape of the US Census Bureau regions for the US
    shapefile_path = "cb_2018_us_region_500k/cb_2018_us_region_500k.shp"

    #Reading the file using geopandas read_file function and then sorting the regions so that they are in alphabetical order
    gdf = gpd.read_file(shapefile_path).sort_values(by = 'NAME')

    unemployment_rates = rpc.output_regional_unemployment(date)

    gdf['Unemployment Rate'] = unemployment_rates

    # Create a plot using matplotlib subplots function
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the GeoDataFrame using geopandas plot function
    gdf.plot(ax=ax, edgecolor='black', column='Unemployment Rate', cmap='coolwarm', legend=True)

    #Setting the coordinates where unemployment rates will be displayed manually (indexing into the unemployment_rates list)
    ax.text(-93, 42, f"{unemployment_rates[0]}%", fontsize=10, ha='center', fontweight = 'bold') #Setting Midwest
    ax.text(-74, 42.5, f"{unemployment_rates[1]}%", fontsize=10, ha='center', fontweight = 'bold') #Setting Northeast
    ax.text(-90, 33, f"{unemployment_rates[2]}%", fontsize=10, ha='center', fontweight = 'bold') #Setting South
    ax.text(-112, 40, f"{unemployment_rates[3]}%", fontsize=10, ha='center', fontweight = 'bold') #Setting West

    ax.set_xlim(-125, -66)  # Longitude bounds
    ax.set_ylim(25, 50) # Latitude bounds

    # Set plot title and labels
    ax.set_title('Unemployment Rates by US Census Bureau Region for ' + date, fontweight = 'bold')
    ax.set_xlabel('Longitude', fontweight = 'bold')
    ax.set_ylabel('Latitude', fontweight = 'bold')

    return fig



def output_spatial_inflation(date):
    """
    This function creates a spatial plot of the inflation rate for a given date. It uses the RegionalPhillipsCurve module to get 
    the inflation rate for each region in the US and puts it on a heatmap using geopandas and matplotlib.

    Inputs: date - a string in the format 'YYYY-MM-01'

    Outputs: A matplotlib plot of the unemployment rate for each region in the US.
    """

    #Getting the shape of the US Census Bureau regions for the US
    shapefile_path = "cb_2018_us_region_500k/cb_2018_us_region_500k.shp"

    #Reading the file using geopandas read_file function
    gdf = gpd.read_file(shapefile_path).sort_values(by = 'NAME')

    inflation_rates = rpc.output_regional_inflation(date)

    gdf['Inflation Rate'] = inflation_rates

    # Create a plot using matplotlib subplots function
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the GeoDataFrame using geopandas plot function
    gdf.plot(ax=ax, edgecolor='black', column='Inflation Rate', cmap='coolwarm', legend=True)

    #Setting the coordinates where unemployment rates will be displayed manually (indexing into the unemployment_rates list)
    ax.text(-93, 42, f"{inflation_rates[0]}%", fontsize=10, ha='center', fontweight = 'bold') #Setting Midwest
    ax.text(-74, 42.5, f"{inflation_rates[1]}%", fontsize=10, ha='center', fontweight = 'bold') #Setting Northeast
    ax.text(-90, 33, f"{inflation_rates[2]}%", fontsize=10, ha='center', fontweight = 'bold') #Setting South
    ax.text(-112, 40, f"{inflation_rates[3]}%", fontsize=10, ha='center', fontweight = 'bold') #Setting West

    ax.set_xlim(-125, -66)  # Longitude bounds
    ax.set_ylim(25, 50) # Latitude bounds

    # Set plot title and labels
    ax.set_title('Inflation Rates by US Census Bureau Region for ' + date, fontweight = 'bold')
    ax.set_xlabel('Longitude', fontweight = 'bold')
    ax.set_ylabel('Latitude', fontweight = 'bold')

    return fig


# output_spatial_unemployment('2020-01-01')






