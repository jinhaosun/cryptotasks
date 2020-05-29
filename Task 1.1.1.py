import pandas as pd
import requests
import json
import datetime

timestamp = []
date_string = ["04/01/2017", "04/01/2020"]
for i in range(len(date_string)):
	date = datetime.datetime.strptime(date_string[i], "%m/%d/%Y")
	timestamp.append(int(datetime.datetime.timestamp(date)))
print(timestamp)

#Get data from web
url_1 = 'https://min-api.cryptocompare.com/data/v2/histohour?\
fsym=BTC&tsym=USDT&start_time=1491019200&end_time=1585713600&e=binance'
result = requests.get(url_1)
api = result.text

# Re-format the data to make it readable
dictionary = json.dumps(result.json(), sort_keys = True, indent = 4)

# Convert data into dataframe
result_json = result.json()
df = pd.DataFrame(result_json['Data']['Data'])
df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')
df.index = pd.to_datetime(df.time)
del df['time']
del df['conversionType']
del df['conversionSymbol']

# Export to .CSV file
df.to_csv('BTC_USDT_1h.csv',index=True)
