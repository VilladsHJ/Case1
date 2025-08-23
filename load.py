import requests
import pandas as pd
import json
import parquet
import pyarrow as pa
import pyarrow.parquet as pq

# URL til en API-endpoint
url = "https://api.energidataservice.dk/dataset/Elspotprices"

response = requests.get(url)  # sender en GET-forespørgsel
data = response.json()        # konverterer svaret til en Python dict

#for key in data["records"]:
#    print(key)
column_names = [] #['HourUTC', 'HourDK', 'PriceArea', 'SpotPriceDKK', 'SpotPriceEUR']
for names in data["records"][0]:
    column_names.append(names)
df_elspotprices = pd.DataFrame(data["records"][:])

pa_elspotprices = pa.Table.from_pandas(df_elspotprices)

pq.write_table(pa_elspotprices, 'elspotprices')

#print(df_elspotprices)
#print(pa_elspotprices)