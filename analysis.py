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

    df_elspotprices = pd.merge(df_elspotprices, df_average) # Merge data frames (inserting average for each time for each area)
    df_elspotprices.insert(len(df_elspotprices.keys()), "IsBelowAvg", df_elspotprices["AverageSpotPricesDKK"]>df_elspotprices["SpotPriceDKK"]) # Inserting column "IsBelowAvg" into dataframe

    return df_elspotprices

print(analysis_script())

