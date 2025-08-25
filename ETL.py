import datetime as dt
import requests
import pandas as pd
import json
import parquet
import pyarrow as pa
import pyarrow.parquet as pq

def ETL_script():
    # URL til en API-endpoint
    url = "https://api.energidataservice.dk/dataset/Elspotprices"

    response = requests.get(url)  # sending a GET request
    response.raise_for_status() # check status codes
    data = response.json()        # Converts the reply to a Python dict

    df_elspotprices = pd.DataFrame(data["records"][:]) # Saves the data as a Pandas data frame

    pa_elspotprices = pa.Table.from_pandas(df_elspotprices) # Converts Pandas data frame to Parquet

    todays_date = dt.date.today()

    pq.write_table(pa_elspotprices, f'elspotprices_{todays_date}') # Saves the daily spot prices to the repository