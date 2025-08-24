import datetime as dt
import requests
import pandas as pd
import json
import parquet
import pyarrow as pa
import pyarrow.parquet as pq

# URL til en API-endpoint
url = "https://api.energidataservice.dk/dataset/Elspotprices"

response = requests.get(url)  # sending a GET request
data = response.json()        # Converts the reply to a Python dict

df_elspotprices = pd.DataFrame(data["records"][:]) # Saves the data as a Pandas data frame

pa_elspotprices = pa.Table.from_pandas(df_elspotprices) # Converts Pandas data frame to Parquet

todays_date = dt.date.today()

pq.write_table(pa_elspotprices, f'elspotprices_{todays_date}') # Saves the daily spot prices to the repository

#filepath = "~/github.com/VilladsHJ/Case1/elspotprices"
#elspotprices = pq.read_table(filepath)
#print(elspotprices)



#print(df_elspotprices)
#print(pa_elspotprices)