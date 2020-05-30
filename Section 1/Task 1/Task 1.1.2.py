import pandas as pd
import requests
import json

#Get data from web
url_2 = 'https://min-api.cryptocompare.com/data/top/mktcapfull?fsym=BTC&tsym=USDT&start_time=2017-04-01&end_time=2020-04-01&e=binance'
result = requests.get(url_2)
api = result.text

# Re-format the data to make it readable
dictionary = json.dumps(result.json(), sort_keys = True, indent = 4)

# Convert data into dataframe
result_json = result.json()
df_top = pd.DataFrame(result_json['Data'])
coin_name = [d.get('FullName') for d in df_top.CoinInfo]

print('Top 10 Coins by Market Cap:')
for i in coin_name:
	print(i)
	
top_10_list = pd.DataFrame({'Coins': coin_name})

# Export to .CSV file
top_10_list.to_csv('Top 10 Coins by Mkt Cap.csv',index=False)
