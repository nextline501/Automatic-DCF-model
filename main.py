import re
import json 
import csv
from io import StringIO
from bs4 import BeautifulSoup
import requests

url_stats = 'https://finance.yahoo.com/quote/{}?p={}'
url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'

##Change Ticker Symbol to view diffrent stock
stock = 'msft'

response = requests.get(url_financials.format(stock, stock))

soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')

script_data = soup.find('script', text=pattern).contents[0]

start = script_data.find('context')-2

json_data = json.loads(script_data[start:-12])

json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()

##print(json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys())

annual_incomeStatement = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
annual_cashflowStatement = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
annual_blanceSheet = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']

##print(annual_is)

annual_cashflow_statement = []
annual_incomeStatement_statement = []
annual_blanceSheet_statement = []

for s in annual_cashflowStatement:
    statement = {}
    for key, val in s.items():
        try:
            ##options are: raw, fmt, longFmt
            statement[key] = val['raw']
        except KeyError:
            continue
        except TypeError:
            continue
    annual_cashflow_statement.append(statement)

##print(annual_cashflow_statement[0])

for s in annual_incomeStatement:
    statement = {}
    for key, val in s.items():
        try:
            ##options are: raw, fmt, longFmt
            statement[key] = val['raw']
        except KeyError:
            continue
        except TypeError:
            continue
    annual_incomeStatement_statement.append(statement)

##print(annual_incomeStatement_statement[0])

for s in annual_blanceSheet:
    statement = {}
    for key, val in s.items():
        try:
            ##options are: raw, fmt, longFmt
            statement[key] = val['raw']
        except KeyError:
            continue
        except TypeError:
            continue
    annual_blanceSheet_statement.append(statement)

## FCF = Net income + intrest expense + 

tax = 0.21
margin_of_safty = 0.15
capex = annual_cashflow_statement[0]['capitalExpenditures']
depri = annual_cashflow_statement[0]['depreciation']
ebit  = annual_incomeStatement_statement[0]['ebit']

_delta_current_assets     = (annual_blanceSheet_statement[0]['totalCurrentAssets'] - (annual_blanceSheet_statement[1]['totalCurrentAssets']))
_delta_current_liabilites = (annual_blanceSheet_statement[0]['totalCurrentLiabilities'] - (annual_blanceSheet_statement[1]['totalCurrentLiabilities']))
change_in_current_asset   = ((_delta_current_assets) - (_delta_current_liabilites))

print("_______________________________________________________________")
print()
print("!CURRENT STOCK: " + stock)
print()
print("Tax rate: " + str(tax) + " %")
print("EBIT: " + str(ebit))
print("Depreciation and Amortization: " + str(depri))
print("CAPEX: " + str(capex))
print("Change in (Current Assets - Current Liabilites): " + str(change_in_current_asset))
print()
fcf = ((ebit * (1-tax)) + (depri) - (capex) - (change_in_current_asset)) * (1 - margin_of_safty)

print("Free cashflow: " + str(fcf))
print()