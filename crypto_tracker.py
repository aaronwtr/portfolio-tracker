from binance.client import Client
import os
from python_bitvavo_api.bitvavo import Bitvavo


"""
Note that this module can not account for staking gains as of yet.
"""

class BinanceFunctions:

    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')     # Fetch API keys
        self.api_secret = os.getenv('BINANCE_SECRET_KEY')

        self.client = Client(self.api_key, self.api_secret)  # Login

    def get_balances(self):
        info = self.client.get_account()
        allBalances = info['balances']
        actualBalances = {}
        BTCtoEuro = float(self.client.get_avg_price(symbol='BTCEUR')['price'])
        USDTtoEuro = float(self.client.get_avg_price(symbol='EURUSDT')['price'])
        print("Fetching Binance wallet data...")
        for bal in allBalances:
            if not bal['free'] == bal['locked']:
                asset = bal['asset']
                quantity = float(bal['free']) + float(bal['locked'])

                if asset == 'EUR':
                    btcvalue = quantity / BTCtoEuro
                    eurovalue = quantity
                if asset == 'USDT' or asset == 'BUSD':
                    continue

                if asset == 'BTC':
                    btcvalue = quantity
                    eurovalue = btcvalue * BTCtoEuro
                else:
                    try:
                        btcvalue = float(self.client.get_avg_price(symbol=asset + 'BTC')['price']) * quantity
                        eurovalue = btcvalue * BTCtoEuro
                    except:
                        pass
                    try:
                        btcvalue = float(self.client.get_avg_price(symbol=asset + 'BNB')['price']) * quantity
                        btcvalue = float(self.client.get_avg_price(symbol='BNBBTC')['price']) * btcvalue
                        eurovalue = btcvalue * BTCtoEuro
                    except:
                        pass

                    try:
                        eurovalue = float(self.client.get_avg_price(symbol=asset + 'EUR')['price']) * quantity
                        btcvalue = eurovalue / BTCtoEuro
                    except:
                        pass

                    try:
                        usdtvalue = float(self.client.get_avg_price(symbol=asset + 'USDT')['price']) * quantity
                        eurovalue = usdtvalue / USDTtoEuro
                        btcvalue = eurovalue / BTCtoEuro
                    except:
                        pass

                actualBalances[asset] = round(eurovalue, 2)

        return actualBalances

class BitvavoFunctions:
    def __init__(self):
        self.bitvavo = Bitvavo({
            'APIKEY': os.getenv('BITVAVO_API_KEY'),
            'APISECRET': os.getenv('BITVAVO_SECRET_KEY'),
            'RESTURL': 'https://api.bitvavo.com/v2',
            'WSURL': 'wss://ws.bitvavo.com/v2/',
            'ACCESSWINDOW': 10000,
            'DEBUGGING': False
        })

    def get_balances(self):
        print('Fetching Bitvavo data...')
        balances = self.bitvavo.balance({})
        tickers = self.bitvavo.tickerPrice({})

        actualBalances = {}
        for crypto_dict in balances:
            crypto_sym = crypto_dict['symbol']
            crypto_sym_check = '{}-EUR'.format(crypto_sym)
            for ticker_dict in tickers:
                ticker_sym = ticker_dict['market']
                if crypto_sym_check == ticker_sym:
                    actualBalances[crypto_sym] = round(float(crypto_dict['available'])*float(ticker_dict['price']), 2)

        return actualBalances
