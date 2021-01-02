import re
import json 
import csv
from io import StringIO
from bs4 import BeautifulSoup
import requests

url_stats = 'https://finance.yahoo.com/quote/{}?p={}'
url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'

stock = 'AAPL'

response = requests.get(url_financials.format(stock, stock))

soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')

script_data = soup.find('script', text=pattern).contents[0]

start = script_data.find('context')-2

json_data = json.loads(script_data[start:-12])

json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()

annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']

annual_cf_statement = []

for s in annual_is:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except KeyError:
            continue
        except TypeError:
            continue
    annual_cf_statement.append(statement)

##print(annual_cf_statement[0])

print("Ebit: " + str(annual_cf_statement[0]['ebit']))
print("Net income: " + str(annual_cf_statement[0]['netIncome']))
print("Gross Profit: " + str(annual_cf_statement[0]['grossProfit']))
