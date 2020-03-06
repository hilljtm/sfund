# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
from IPython import get_ipython


#%%
# Crypto heatmap with coinbase 


#%%
import requests 
import pandas as pd 
import matplotlib.pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')


#%%
url = "https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&limit=10&e=Coinbase"
f = requests.get(url)
ipdata = f.json()
pd.DataFrame(ipdata['Data']).head(5)


#%%
def get_data(date):
    """query API for 2000 days historical price data starting from "date"."""
    url = "https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&limit=2000&toTs={}".format(date)
    r = requests.get(url)
    ipdata = r.json()
    return ipdata 


#%%
def get_df(from_date, to_date):
    date = to_date
    holder = []
    # while earliest date returned is later than the earliest data requested, keep querying API # and adding results to list 
    while date > from_date:
        data = get_data(date)
        holder.append(pd.DataFrame(data['Data']))
        date = data['TimeFrom']
        # join together all api queries from list 
        df = pd.concat(holder, axis=0)
        # remove data points from before from_date
        df = df[df['time']>from_date]
        # convert to timestamp readable date format
        df['time'] = pd.to_datetime(df['time'], unit='s')
        # make datafrom index the time
        df.set_index('time', inplace=True)
        # sort so its in time order
        df.sort_index(ascending=False, inplace=True)
        return df


#%%
df = get_df(1504435200, 1566162039)


#%%
fig, ax = plt.subplots(figsize=(15, 10))
ax.plot(df[['low', 'close', 'high']])
ax.set_ylabel('BTC Price (USD)')
ax.set_xlabel('Date')
ax.legend(['Low', 'Close', 'High']);


#%%
def get_data_spec(coin, date, time_period):
    """query api for 2000 units historical price data starting from "date"."""
    url = "https://min-api.cryptocompare.com/data/{}?fsym={}&tsym=USD&Limit=2000&toTs={}".format(time_period, coin, date)
    r = requests.get(url)
    ipdata = r.json()
    return ipdata


#%%
def get_df_spec(time_period, coin, from_date, to_date):
    """ get historical price data between two dates. If further apart than query limit then query multiple times"""
    date = to_date
    holder = []
    while date > from_date:
        data = get_data_spec(coin, date, time_period) 
        holder.append(pd.DataFrame(data['Data']))
        date = data['TimeFrom'] 
    df = pd.concat(holder, axis = 0)
    df = df[df['time']>from_date]
    df['time'] = pd.to_datetime(df['time'], unit='s') 
    df.set_index('time', inplace=True)
    df.sort_index(ascending=False, inplace=True)
    # keep the close price, with column heading as name of coin. 
    df.rename(columns={'close':coin}, inplace=True)
    return df[coin]


#%%
coins = ['BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'BNB', 'USDT', 'EOS', 'XMR', 'XLM', 'ADA']


#%%
holder = []
from_date = 1565481600 # last week
to_date = 1536081800   # today
time_period = 'histhour'
for coin in coins:
    holder.append(get_df_spec(time_period, coin, from_date, to_date))
df = pd.concat(holder, axis = 1)    


#%%
# convert each column of df to be rate of return instead of price
df = df.divide(df.shift())-1


#%%
import seaborn as sns 
plt.figure(figsize=(9,5))
sns.heatmap(df.corr(), annot=True, linewidth=0.5, cmap='coolwarm');


#%%



