import requests
import pandas as pd
import json
import parquet
import pyarrow as pa
import pyarrow.parquet as pq
from ETL import pa_elspotprices

elspotprices = pa_elspotprices
print(elspotprices)

