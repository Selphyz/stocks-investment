#%%
import pandas as pd
import numpy as np
import yfinance as yf
#%%
df = yf.download(tickers=['AAPL', 'MSFT'], period='1y', interval='1wk')
#%%
df.head()
#%%
df.Close
#%%
