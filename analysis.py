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

filepath = "~/github.com/VilladsHJ/Case1/elspotprices_2025-08-24" # path to the spot prices from the repository
elspotprices = pq.read_table(filepath)  # saving data to data a pyarrow data frame

df_elspotprices = elspotprices.to_pandas() # Converting to pandas data frame

average_prices = df_elspotprices.groupby("HourUTC")["SpotPriceDKK"].mean().round() # Finding average of spotprices (rounds to nearest whole number)

unique_hours = list(df_elspotprices.groupby("HourUTC")["HourDK"].indices.keys()) # Finds each unique hour

df_average_prices = average_prices.to_frame() # Convert to Pandas dataframe

list_average_prices = df_average_prices["SpotPriceDKK"].to_list() # convers prices to a list


dict_average = {"HourUTC": unique_hours,
                'AverageSpotPricesDKK': list_average_prices} # Create dictionary for dataframe with only hour and average spot price


df_average = pd.DataFrame(dict_average) # creates pandas dataframe with HoutUTC and Average prices

list_below_avg = []
for q in range(len(df_average["HourUTC"])): # Loop through unique timestamp
    for i in range(len(df_elspotprices["HourUTC"])): # Loop through timestamps for all spotprices
        if df_average["HourUTC"][q] == df_elspotprices["HourUTC"][i]: # check if timestamp is equal
            list_below_avg.append(df_average["AverageSpotPricesDKK"][q]>df_elspotprices["SpotPriceDKK"][i]) # append Boolean ("true" if spot price is below average) 

df_elspotprices.insert(len(df_elspotprices.keys()), "IsBelowAvg", list_below_avg) # Inserting column into dataframe

app = Dash() # initialize Dash app

fig1 = px.bar(df_elspotprices, x="HourUTC", y="SpotPriceDKK", color="PriceArea", barmode="group") # First bar plot with grouped prices
fig2 = px.bar(df_average, x="HourUTC", y="AverageSpotPricesDKK", color="AverageSpotPricesDKK") # second bar plot with average prices

app.layout = html.Div([
        html.Div([
            html.H1("Grouped Spot Prices"),
            html.Div('''Grouped spot prices during the day'''),
            dcc.Graph(id='Grouped', figure=fig1)
        ]),
        html.Div([
            html.H1("Average Spot Prices"),
            html.Div('''Average spot prices during the day 
                     (rounded to nearest whole number)'''),
            dcc.Graph(id='Average', figure=fig2)]),

])

if __name__ == '__main__':
    app.run(debug=True)




