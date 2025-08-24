import requests
import pandas as pd
import json
import parquet
import pyarrow as pa
import pyarrow.parquet as pq


filepath = "~/github.com/VilladsHJ/Case1/elspotprices"
elspotprices = pq.read_table(filepath)
print(elspotprices)

