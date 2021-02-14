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
print("Enter stock ticker: ")
stock = str(input())

response = requests.get(url_financials.format(stock, stock))

soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')

script_data = soup.find('script', text=pattern).contents[0]

start = script_data.find('context')-2

json_data = json.loads(script_data[start:-12])

json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()

##print(json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory'].keys())
##print(json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements'])

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

##Manual indata

print("Enter tax (ex. 0.21): ")
tax = float(input())
print("Enter margin of safty (ex. 0.15): ")
margin_of_safty = float(input())
print("Enter risk free return (ex. 0.01): ")
risk_free_return = float(input())
print("Enter expected return (ex. 0.15): ")
expected_return = float(input())
print("Enter cost of debt (ex. 0.035): ")
cost_of_debt = float(input())
print("Enter perpetuity growth (ex. 0.03): ")
perpetuity_growth = float(input())

market_cap = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['marketCap']['raw']
ask_price = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['ask']['raw']
number_of_shares = market_cap/ask_price

equity = annual_blanceSheet_statement[0]['totalStockholderEquity']

if(stock == "fb"):
    debt = 0
else:
    debt = annual_blanceSheet_statement[0]['longTermDebt']

beta = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['beta']['raw']
capex = annual_cashflow_statement[0]['capitalExpenditures']
depri = annual_cashflow_statement[0]['depreciation']
ebit  = annual_incomeStatement_statement[0]['ebit']

_delta_current_assets     = (annual_blanceSheet_statement[0]['totalCurrentAssets'] - (annual_blanceSheet_statement[1]['totalCurrentAssets']))
_delta_current_liabilites = (annual_blanceSheet_statement[0]['totalCurrentLiabilities'] - (annual_blanceSheet_statement[1]['totalCurrentLiabilities']))
change_in_current_asset   = ((_delta_current_assets) - (_delta_current_liabilites))

CAPM = risk_free_return + beta * expected_return
WACC = ((debt/(debt+equity)) * (cost_of_debt) * (1-tax) + (equity/(debt+equity))) * CAPM
fcf = ((ebit * (1-tax)) + (depri) - (capex) - (change_in_current_asset)) * (1 - margin_of_safty)

P0 = fcf/(WACC-perpetuity_growth)
price_target = P0/number_of_shares 

print("_______________________________________________________________")
print()
print("!CURRENT STOCK: " + stock)
print()
print("Risk free rate: " + str(risk_free_return))
print("Beta: " + str(beta))
print("Expected_return: " + str(expected_return))
print("CAPM: " + str(CAPM))
print()
print("Total equity: " + str(equity))
print("Debt: " + str(debt))
print("Tax rate: " + str(tax) + " %")
print("Cost of debt: " + str(cost_of_debt))
print("Cost of Equity: " + str(CAPM))
print("WACC: " + str(WACC))
print()
print("Number of shares: " + str(number_of_shares))
print("EBIT: " + str(ebit))
print("Depreciation and Amortization: " + str(depri))
print("CAPEX: " + str(capex))
print("Change in (Current Assets - Current Liabilites): " + str(change_in_current_asset))
print()
print("Free cashflow: " + str(fcf))
print("P0: " + str(P0))
print()
print("Current price of " + stock + " " + str(ask_price))
print("DCF Price Target: " + str(price_target) + " USD")
print("EBIT x 10 ref: " + str((ebit * 10)/number_of_shares)+ " USD")
print("EBIT x 15 ref: " + str((ebit * 15)/number_of_shares)+ " USD")
print("EBIT x 20 ref: " + str((ebit * 20)/number_of_shares)+ " USD")