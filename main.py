import datetime as dt
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
from analysis import df_elspotprices, df_average

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

#if __name__ == '__main__':
#    app.run(debug=True)