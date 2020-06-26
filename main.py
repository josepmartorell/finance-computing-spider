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

for ticker in range(500):
    wikiSplit = wikiResponse.text.split("external text")[i]
    wikiSplitAgain = wikiSplit.split(">")[1]
    wikiTicker = wikiSplitAgain.split("<")[0]
    data["Company"].append(wikiTicker)
    i += 2

data.update(data)

df = pd.DataFrame(data)

print(data)

# todo: in development...
