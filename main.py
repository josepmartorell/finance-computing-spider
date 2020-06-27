# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

import requests
import pandas as pd

wikiURL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
wikiResponse = requests.get(wikiURL)
data = {"Company": []}
i = 1

for ticker in range(5):  # 10 instead of 500 for testing purposes
    wikiSplit = wikiResponse.text.split("external text")[i]
    wikiSplitAgain = wikiSplit.split(">")[1]
    wikiTicker = wikiSplitAgain.split("<")[0]
    data["Company"].append(wikiTicker)
    i += 2

Indicators = {"Previous Close": [],
              "Open": [],
              "Bid": [],
              "Ask": [],
              "Day&#x27;s Range": [],
              "52 Week Range": [],
              "Volume": [],
              "Avg. Volume": [],
              "Market Cap": [],
              "Beta": [],
              "PE Ratio (TTM)": [],
              "EPS (TTM)": [],
              "Earnings Date": [],
              "Dividend &amp; Yield": [],
              "Ex-Dividend Date": [],
              "1y Target Est": []}

for tickerSymbol in data["Company"]:
    url = ("http://finance.yahoo.com/quote/" + tickerSymbol
           + "?p=" + tickerSymbol)
    response = requests.get(url)
    htmlText = response.text
    for indicator in Indicators:
        try:
            yahooSplit = htmlText.split(indicator)[1]
            yahooSplitAgain = yahooSplit.split('</span>')[1]
            yahooSplitAnother = yahooSplitAgain.split("reactid=")[2]
            yahooIndicator = yahooSplitAnother.split("\">")[1]
            Indicators[indicator].append(yahooIndicator)
        except:
            Indicators[indicator].append("N/A")

data.update(Indicators)
df = pd.DataFrame(data)
print(df.head())
print(df.tail())

# todo: in development...
