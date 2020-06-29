# -*- coding: utf-8 -*-
"""
@author: jmartorell
"""

import requests
import pandas as pd


def render_csv(data):
    CSV = "\n".join([k + ',' + ",".join(v) for k, v in data.items()])
    return CSV


class App:
    def __init__(self):
        self.wikiURL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self.wikiResponse = requests.get(self.wikiURL)
        self.data = {"Company": []}
        self.position = 1
        self.indicators = {"Previous Close": [],
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

    def extract_tickers(self, ranges):
        for ticker in range(ranges):  # 10 instead of 500 for testing purposes
            wiki_split1 = self.wikiResponse.text.split("external text")[self.position]
            wiki_split2 = wiki_split1.split(">")[1]
            wiki_ticker = wiki_split2.split("<")[0]
            self.data["Company"].append(wiki_ticker)
            self.position += 2

    def cross_databases(self, scope):
        self.extract_tickers(scope)
        for tickerSymbol in self.data["Company"]:
            url = ("http://finance.yahoo.com/quote/" + tickerSymbol
                   + "?p=" + tickerSymbol)
            response = requests.get(url)
            html_text = response.text
            for indicator in self.indicators:
                try:
                    if indicator == "Day&#x27;s Range" or indicator == "52 Week Range" \
                            or indicator == "Dividend &amp; Yield":
                        yahoo_split1 = html_text.split(indicator)[1]
                        yahoo_split2 = yahoo_split1.split('</span>')[1]
                        yahoo_split3 = yahoo_split2.split("reactid=")[1]
                        yahoo_split4 = yahoo_split3.split("</td>")[0]
                        yahoo_split5 = yahoo_split4.split("\">")[1]
                        self.indicators[indicator].append(yahoo_split5)
                    else:
                        yahoo_split1 = html_text.split(indicator)[1]
                        yahoo_split2 = yahoo_split1.split('</span>')[1]
                        yahoo_split3 = yahoo_split2.split("reactid=")[2]
                        yahoo_split4 = yahoo_split3.split("\">")[1]
                        self.indicators[indicator].append(yahoo_split4)
                except:
                    self.indicators[indicator].append("N/A")


if __name__ == '__main__':
    app = App()
    # spider run mode selector
    switch = int(input('\nSWITCH SPIDER RUN MODE:\n\t'
                       '- TEST........(0 + Enter)\n\t'
                       '- TRACKER.....(1 + Enter)\n'))

    if switch != 0:
        app.cross_databases(500)
        app.data.update(app.indicators)
        df = pd.DataFrame(app.data)
        df.to_csv(r"stock.csv")
        df.to_json(r"stock.json", orient="index", indent=4)
    else:
        print("\nTracking test sample ...")
        app.cross_databases(10)
        app.data.update(app.indicators)
        df = pd.DataFrame(app.data)
        print("Screening shortened head sample ...\n")
        print(df.head())
        pd.options.display.max_columns = None
        print("\nScreening full columns display ...\n")
        print(df)
        print("\nScreening compacted information ...\n")
        print(render_csv(df))
        print("\nRendering data to csv ...")
        df.to_csv(r"stock.csv")
        print("Rendering data to json ...\n")
        df.to_json(r"stock.json", orient="index", indent=4)

    # todo: in development...
    #  spider challenge: https://www.freeformatter.com/json-formatter.html
