from dash import Dash, html, dcc
import plotly.express as px
import ETL
from analysis import analysis_script

app = Dash() # initialize Dash app

def dashboard():
    df_elspotprices = analysis_script()
    fig1 = px.bar(df_elspotprices, x="HourUTC", y="SpotPriceDKK", color="PriceArea", barmode="group", hover_data="IsBelowAvg") # First bar plot with grouped prices
    fig2 = px.bar(df_elspotprices, x="HourUTC", y="AverageSpotPricesDKK", color="AverageSpotPricesDKK",barmode="overlay") # Second bar plot with average prices

    fig1.add_scatter(x=df_elspotprices["HourUTC"], y=df_elspotprices["AverageSpotPricesDKK"], mode="lines", name="Average Spot Price")

    app.layout = html.Div([
            html.Div([
                html.H1("Grouped Spot Prices"),
                html.Div('''Spot prices for each area during the day. Trendline showing the average spot price'''),
                dcc.Graph(id='Grouped', figure=fig1)
            ]),
            html.Div([
                html.H1("Average Spot Prices"),
                html.Div('''Average spot prices during the day 
                        (rounded to nearest whole number)'''),
                dcc.Graph(id='Average', figure=fig2)]),

    ])

if __name__ == '__main__':
    ETL.ETL_script()
    dashboard()
    #app.run(debug=True)