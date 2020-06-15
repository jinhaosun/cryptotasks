import pandas as pd
import json
import datetime
import urllib

def get_url(timeframe):
	if timeframe == 'daily':
		return 'https://min-api.cryptocompare.com/data/v2/histoday?'
	if timeframe == 'hourly':
		return 'https://min-api.cryptocompare.com/data/v2/histohour?'

def set_parameter(url_parameter):
	parameter = dict()
	parameter['fsym'] = url_parameter['fsym']
	parameter['tsym'] = url_parameter['tsym']
	parameter['limit'] = url_parameter['limit']
	parameter['toTs'] = url_parameter['toTs']
	parameter['api_key'] = url_parameter['api_key']
	return(urllib.parse.urlencode(parameter))

beginning_timestamp = 1483261200

def get_data(url_timeframe, url_parameter, earliest_timestamp):
	if earliest_timestamp < beginning_timestamp:
		return None
	else:
		url_parameter['toTs'] = earliest_timestamp
		url = url_timeframe + set_parameter(url_parameter)
		result = urllib.request.urlopen(url)
		data = result.read().decode()
		return data
	
def main():
	api_key = '54da7011bb520e0898005fd175069e08b058cd6f429d65779a3c91106e55d42f'
	url_timeframe = get_url('hourly')
	url_parameter = {'fsym': 'BTC', 'tsym': 'USDT', 'limit': 2000, 'api_key': api_key}
	earliest_timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))
	all_data = []
	
	while True:
		data = get_data(url_timeframe, url_parameter, earliest_timestamp)
		if data is None:
			break
		else:
			js = json.loads(data)
			earliest_timestamp = js['Data']['TimeFrom']-1
			all_data.append(js['Data']['Data'])

	# Convert all data into dataframe
	df = pd.concat([pd.DataFrame(d) for d in all_data])
	
	df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')
	df = df.sort_values(by='time', ascending=False)
	df = df.reset_index(drop=True)
	
	# Select data in the past 3 years
	df = df[:26305]
	
	df.index = pd.to_datetime(df.time)
	del df['time']
	del df['conversionType']
	del df['conversionSymbol']
	
	# Export to .CSV file
	df.to_csv('BTC_USDT_3yr_hourly.csv',index=True)
	
if __name__ == '__main__':
	main()
