import os
import pandas as pd
from degiro_tracker import DegiroFunctions


class DegiroUpdateCSV:
    def __init__(self):
        with open("len_products.txt", "r") as f:
            self.products = int(f.read())

    def update_stocks(self):
        portfolio_path = os.getenv("PORTFOLIO_CSV")

        stocks_portfolio = pd.read_excel(portfolio_path, sheet_name='Stocks portfolio', header=13, usecols="A:J",
                                         nrows=self.products)

        print(stocks_portfolio)
