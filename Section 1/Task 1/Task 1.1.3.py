import pandas as pd
import requests

class CoinData:
	
	def GetAPI_HistHour(self, url_1):
		result = requests.get(url_1)
		# Convert data into dataframe
		result_json = result.json()
		histhr = pd.DataFrame(result_json['Data']['Data'])
		histhr['time'] = pd.to_datetime(histhr['time'].astype(int), unit='s')
		histhr.index = pd.to_datetime(histhr.time)
		del histhr['time']
		del histhr['conversionType']
		del histhr['conversionSymbol']
		return histhr
		
	def GetAPI_Toplist_MktCap(self, url_2):
		result1 = requests.get(url_2)
		# Convert data into dataframe
		result_json1 = result1.json()
		toplist = pd.DataFrame(result_json1['Data'])
		coin_name = [d.get('FullName') for d in toplist.CoinInfo]
		
		print('Top 10 Coins by Market Cap:')
		for i in coin_name:
			print(i)
		
		top_10_list = pd.DataFrame({'Coins': coin_name})
		return top_10_list
			
def main():
	url_1 = 'https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USDT&start_time=2017-04-01&end_time=2020-04-01&e=binance'
	url_2 = 'https://min-api.cryptocompare.com/data/top/mktcapfull?fsym=BTC&tsym=USDT&start_time=2017-04-01&end_time=2020-04-01&e=binance'
	coin_data = CoinData()
	coin_data.GetAPI_HistHour(url_1).to_csv('BTC_USDT_1h.csv',index=True)
	coin_data.GetAPI_Toplist_MktCap(url_2).to_csv('Top 10 Coins by Mkt Cap.csv',index=False)
  						        
if __name__ == '__main__':
    main()
	