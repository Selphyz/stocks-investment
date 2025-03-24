#%%
from io import StringIO

import numpy as np
import pandas as pd
import requests
#%%
csv = requests.get('https://cloud.appwrite.io/v1/storage/buckets/675c32340014863cd93c/files/675c4546002251538adb/download?project=laiatec&project=laiatec&mode=admin')
csv.content
#%%
df = pd.read_csv(csv.content, sep=',', encoding='latin-1',
                 dtype={'lsttv': float})
df.head()
#%%
if csv.status_code == 200:
    # Cargar los datos en un DataFrame
    data = StringIO(csv.text)
    df = pd.read_csv(data)
    print(df)
else:
    print(f"Error al descargar los datos: {csv.status_code}")