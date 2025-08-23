import requests
import pandas as pd
import json
import parquet as pq
import pyarrow as pa

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
        

print(df_elspotprices)
print(pa_elspotprices)