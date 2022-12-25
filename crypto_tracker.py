from binance.client import Client
from python_bitvavo_api.bitvavo import Bitvavo
import os
from currency_converter import CurrencyConverter

"""
Note that this module can not account for staking gains as of yet.
"""


class BinanceFunctions:

    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')  # Fetch API keys
        self.api_secret = os.getenv('BINANCE_SECRET_KEY')

        self.client = Client(self.api_key, self.api_secret)  # Login

    def get_balances(self):
        print('Fetching Binance data...')
        assets = self.client.get_account()['balances']
        prices_usd = self.client.get_all_tickers()
        binance_wallet_temp = {}
        for asset in assets:
            if float(asset['free']) != 0.00000000:
                binance_wallet_temp[asset['asset']] = asset['free']
            elif float(asset['locked']) != 0.00000000:
                binance_wallet_temp[asset['asset']] = asset['locked']
            else:
                continue

        wallet_sym1 = list(binance_wallet_temp.keys())

        # We will now remove the LD part of the tickers. Note that this will affect cryptocurrencies that have LD as
        # their starting letters.

        binance_wallet_amount = {}
        for sym1 in wallet_sym1:
            if sym1[0:2] == 'LD' and sym1[2:] not in binance_wallet_temp:
                binance_wallet_amount[str(sym1[2:])] = float(binance_wallet_temp[sym1])
            elif sym1[2:] in binance_wallet_temp:
                binance_wallet_amount[str(sym1[2:])] = (float(binance_wallet_temp[sym1]) +
                                                        float(binance_wallet_temp[sym1[2:]]))
            else:
                binance_wallet_amount[sym1] = float(binance_wallet_temp[sym1])

        cc = CurrencyConverter()
        wallet_keys = list(binance_wallet_amount.keys())
        binance_wallet = {}
        for asset in wallet_keys:
            for pair in prices_usd:
                if pair['symbol'] == '{}USDT'.format(asset):
                    binance_wallet[asset] = round(
                        cc.convert(float(binance_wallet_amount[asset]) * float(pair['price']), 'USD', 'EUR'), 2)

        return binance_wallet
        # DEBUG: FIND A WAY TO IMPLEMENT FIXED PRODUCTS


class BitvavoFunctions:
    def __init__(self):
        self.bitvavo = Bitvavo({
            'APIKEY': os.getenv('BITVAVO_API_KEY'),
            'APISECRET': os.getenv('BITVAVO_SECRET_KEY'),
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
