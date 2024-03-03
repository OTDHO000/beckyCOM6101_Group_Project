# download xml from API-source, if the last number 5 digit is 1 in the api url, it means the data is in the first day of the month
import urllib.request
import datetime
import pandas as pd

# default column name is 'api_url'
api_source = pd.read_csv('restaurant-info-hk/xml/API-source/api-source.csv', encoding='utf-8', names=['api_url'])

# filter the api source which is in the first day of the month, by checking the last number 6 digit of the api url
api_source = api_source[api_source['api_url'].str[-6] == '1']

# export api source to csv file
api_source.to_csv('restaurant-info-hk/xml/API-source/api-source_1.csv', index=False, header=False)

# download the xml file from api source, file name is the last 12 digit of the api url
for index, row in api_source.iterrows():
    url = row['api_url']
    file_name = url[-12:]
    urllib.request.urlretrieve(url, 'restaurant-info-hk/xml/' + file_name + '.xml')
    print(file_name + ' downloaded')
    
# python restaurant-info-hk\xml\download-xml-from-api.py