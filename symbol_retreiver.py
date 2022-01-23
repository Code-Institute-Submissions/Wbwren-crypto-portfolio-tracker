import urllib
from urllib import request
import json
from csv import reader
import csv
import os

api_key = os.environ.get('NOMICS_API_KEY')

url = "https://api.nomics.com/v1/currencies?key=api_key&ids=&attributes=id,name,logo_url\\"
    
    

details = urllib.request.urlopen(url).read()
decoded_string = details.decode()
    
res = json.loads(decoded_string)
with open('ticker_symbols.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for coin in res:
        writer.writerow([coin['id']])