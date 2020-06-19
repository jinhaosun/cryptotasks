import pandas as pd
import json
import requests
import urllib

def get_url():
	return 'https://min-api.cryptocompare.com/data/top/mktcapfull?'

def set_parameter(url_parameter):
	parameter = dict()
	parameter['fsym'] = url_parameter['fsym']
	parameter['tsym'] = url_parameter['tsym']
	parameter['api_key'] = url_parameter['api_key']
	url_parameter = urllib.parse.urlencode(parameter)
	params = json.dumps(url_parameter)
	return(params)

def get_data(url_parameter):
	url = get_url() + set_parameter(url_parameter)
	result = requests.get(url)
	# Convert data into dataframe
	result_json = result.json()
	toplist = pd.DataFrame(result_json['Data'])
	coin_name = [d.get('FullName') for d in toplist.CoinInfo]
		
	print('Top 10 Coins by Market Cap:')
	for i in coin_name:
		print(i)
		
	top_10_list = pd.DataFrame({'Coins': coin_name})
	return top_10_list

def main():
	api_key = '54da7011bb520e0898005fd175069e08b058cd6f429d65779a3c91106e55d42f'
	url_parameter = {'fsym': 'BTC', 'tsym': 'USDT', 'api_key': api_key}
	get_data(url_parameter).to_csv('Top 10 Coins by Market Cap.csv', index=False)
	
if __name__ == '__main__':
	main()
