from python_bitvavo_api.bitvavo import Bitvavo
import os

"""
Note that this module can not account for staking gains as of yet.
"""

class BitvavoFunctions:
    def __init__(self):
        self.bitvavo = Bitvavo({
            'APIKEY': os.getenv('BITVAVO_API_KEY'),
            'APISECRET': os.getenv('BITVAVO_API_SECRET_KEY'),
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
                    actualBalances[crypto_sym] = round(float(crypto_dict['available']) * float(ticker_dict['price']), 2)

        return actualBalances
