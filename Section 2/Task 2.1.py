import datetime
import pandas as pd
from binance.client import Client

class CoinData:
	
	def API_GetData(self, ticker, start, end):
		
		client = Client("api_key", "api_secret")
		kline = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_30MINUTE, start, end)
		
		dt = []
		
		for i in range(len(kline)): 
			dt.append(datetime.datetime.fromtimestamp(int(kline[i][0])/1000))

		dt = pd.DataFrame(dt)
		df = pd.DataFrame(kline)
		df = df.iloc[:,1:5]
		df = pd.concat([dt, df], axis=1)
		df.columns = ['Time', 'Open', 'High', 'Low', 'Close']
		df.index = pd.to_datetime(df.Time)
		del df['Time']
		
		return df

def main():
	ticker = "ETHBTC"
	start = "2 January, 2018"
	end = "1 May, 2020"
	coin_data = CoinData()
	coin_data.API_GetData(ticker, start, end).to_csv('ETHBTC_30MINS.csv',index=True)
  						        
if __name__ == '__main__':
    main()
