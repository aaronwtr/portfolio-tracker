from binance.client import Client
import os

class BinanceFunctions:

    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')     # Fetch API keys
        self.api_secret = os.getenv('BINANCE_SECRET_KEY')

        self.client = Client(self.api_key, self.api_secret)  # Login

    def fetch_binance_portfolio(self):
        portfolio = self.client.get_account_snapshot(type='SPOT')

        print(portfolio['snapshotVos'][0])
        print(portfolio['snapshotVos'][1])
        print(portfolio['snapshotVos'][2])
        print(portfolio['snapshotVos'][3])
        print(portfolio['snapshotVos'][4])
