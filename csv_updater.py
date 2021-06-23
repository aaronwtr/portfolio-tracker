import os
import pandas as pd


def update_stocks():
    portfolio_path = os.getenv("PORTFOLIO_CSV")

    stocks_portfolio = pd.read_excel(portfolio_path, sheet_name='Stocks portfolio', header=13, usecols="A:J", nrows=)