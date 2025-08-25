import requests
import datetime as dt
import pandas as pd
import json
import parquet
import pyarrow as pa
import pyarrow.parquet as pq
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go


def analysis_script():
    todays_date = dt.date.today()

    #filepath = f"https://github.com/VilladsHJ/Case1/elspotprices_{todays_date}" # path to the spot prices from the repository
    filepath = f"~/github.com/VilladsHJ/Case1/elspotprices_2025-08-25" # path to the spot prices from the repository
    elspotprices = pq.read_table(filepath)  # saving data to data a pyarrow data frame

    df_elspotprices = elspotprices.to_pandas() # Converting to pandas data frame

    average_prices = df_elspotprices.groupby("HourUTC")["SpotPriceDKK"].mean().round() # Finding average of spotprices (rounds to nearest whole number)

    unique_hours = list(df_elspotprices.groupby("HourUTC")["HourDK"].indices.keys()) # Finds each unique hour

    df_average_prices = average_prices.to_frame() # Convert to Pandas dataframe

    list_average_prices = df_average_prices["SpotPriceDKK"].to_list() # Converts prices to a list - This list will be used i


    dict_average = {"HourUTC": unique_hours,
                    'AverageSpotPricesDKK': list_average_prices} # Create dictionary for dataframe with only hour and average spot price


    df_average = pd.DataFrame(dict_average) # Creates pandas dataframe with HourUTC and Average prices from dictionary


    # The for loop below goes through each unique timestamp and loops through all timestamps in df_elspotprices. 
    #   If there is a match on time stamp each spot price for the corresponding time stamp is compared to the average spotprice for that timestamp. 
    #   If the spot price is lower that the average spot a boolean value is stored (TRUE/FALSE) in the list "list_below_avg"
    list_below_avg = []
    list_avg = []
    for q in range(len(df_average["HourUTC"])): # Loop through unique timestamp
        for i in range(len(df_elspotprices["HourUTC"])-1,-1,-1): # Loop through timestamps for all spotprices - added steps to range() to reverse the order to ensure data is stored correctly 
            if df_average["HourUTC"][q] == df_elspotprices["HourUTC"][i]: # check if timestamp is equal
                list_below_avg.append(df_average["AverageSpotPricesDKK"][q]>df_elspotprices["SpotPriceDKK"][i]) # append Boolean ("true" if spot price is below average) 
                list_avg.append(df_average["AverageSpotPricesDKK"][q])

    df_elspotprices.insert(len(df_elspotprices.keys()), "AverageSpotPricesDKK", list_avg[::-1]) # Inserting column "AverageSpotPricesDKK" into dataframe
    df_elspotprices.insert(len(df_elspotprices.keys()), "IsBelowAvg", list_below_avg[::-1]) # Inserting column "IsBelowAvg" into dataframe

    return df_elspotprices


