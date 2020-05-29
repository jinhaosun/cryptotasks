import datetime
import pandas as pd
from binance.client import Client

client = Client("api_key", "api_secret")

# Fetch 1 minute klines for the last day up until now
klines_BNBBTC_1min = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
klines_BTCUSD_30min = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 April, 2020", "1 May, 2020")
klines_XRPBTC_wk = client.get_historical_klines("XRPBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

klines = [klines_BNBBTC_1min, klines_BTCUSD_30min, klines_XRPBTC_wk]

dataframe_klines = []
for i in range(len(klines)):
	datetime.datetime.fromtimestamp(int(klines[i][0][0])/1000)
	df_klines = pd.DataFrame(klines[i])
	df_klines = df_klines.iloc[:,0:5]
	df_klines.columns = ['Time', 'Open', 'High', 'Low', 'Close']
	df_klines.index = pd.to_datetime(df_klines.Time)
	del df_klines['Time']
	dataframe_klines.append(df_klines)

df_1min_candle = dataframe_klines[0]
df_30min_candle = dataframe_klines[1]
df_wk_candle = dataframe_klines[2]

# Export to .CSV files
df_1min_candle.to_csv('BNBBTC df_1min_candle.csv',index=True)
df_30min_candle.to_csv('ETHBTC df_30min_candle.csv',index=True)
df_wk_candle.to_csv('XRPBTC df_wk_candle.csv',index=True)

#%%
# Get market depth
symbol = ['BNBBTC','ETHBTC','XRPBTC']

def Get_Market_Depth(symbol):
	market_depth = client.get_order_book(symbol=symbol)
	return market_depth

depth = []
for i in range(len(symbol)):
	depth.append(Get_Market_Depth(symbol[i]))

# Make to dataframes
dataframe = []
for i in range(len(depth)):
	df = pd.DataFrame(depth[i])
	df.loc[:,'bids'] = df.bids.map(lambda x: x[0])
	df.loc[:,'asks'] = df.asks.map(lambda x: x[0])
	del df['lastUpdateId']
	dataframe.append(df)
	
df_BNBBTC = dataframe[0]
df_ETHBTC = dataframe[1]
df_XRPBTC = dataframe[2]

# Export to .CSV files
df_BNBBTC.to_csv('BNBBTC Orderbook.csv',index=False)
df_ETHBTC.to_csv('ETHBTC Orderbook.csv',index=False)
df_XRPBTC.to_csv('XRPBTC Orderbook.csv',index=False)

#%%
# Get prices for all the pairs.
prices = client.get_all_tickers()
df_prices = pd.DataFrame(prices)

# Export to .CSV file
df_prices.to_csv('Pair Prices.csv',index=False)

#%%
# Get recent trades.
symbol = ['BNBBTC','ETHBTC','XRPBTC']

def Get_Recent_Trade(symbol):
	trade = client.get_recent_trades(symbol=symbol, limit=250)
	return trade

recent_trade = []
for i in range(len(symbol)):
	recent_trade.append(pd.DataFrame(Get_Recent_Trade(symbol[i])))
		
recent_BNBBTC = recent_trade[0]
recent_ETHBTC = recent_trade[1]
recent_XRPBTC = recent_trade[2]

# Export to .CSV files
recent_BNBBTC.to_csv('BNBBTC_Recent Trades.csv', index=False)
recent_ETHBTC.to_csv('ETHBTC_Recent Trades.csv', index=False)
recent_XRPBTC.to_csv('XRPBTC_Recent Trades.csv', index=False)
