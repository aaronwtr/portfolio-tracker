import os
import pandas as pd
import openpyxl as pyxl


class DegiroUpdateCSV:
    def __init__(self):
        with open("len_products.txt", "r") as f:
            self.products = int(f.read())
        f.close()

        self.portfolio_path = os.getenv("PORTFOLIO_CSV")
        self.header_value = 15  # Start of stock portfolio rows

    def get_excel_stocks(self):
        stocks_portfolio = pd.read_excel(self.portfolio_path, sheet_name='Stocks portfolio',
                                         header=self.header_value - 2, usecols="A:J", nrows=self.products)

        excel_stocks = list(stocks_portfolio["Code"])
        stocks_value_old = list(stocks_portfolio["Huidige waarde"])
        dict_old_value = dict(zip(excel_stocks, stocks_value_old))
        return excel_stocks, dict_old_value

    def update_stocks(self, excel_stocks, dict_old_value, DGF, save=False):
        wb = pyxl.load_workbook(filename=self.portfolio_path)
        ws = wb.worksheets[0]

        products = DGF.fetch_portfolio()
        # print(products)
        # ws['E6'].value = products['EUR']

        if not os.path.isfile("len_products.txt"):
            with open("len_products.txt", "w") as f:
                f.write(str(len(products)))
            f.close()

        curr_row = 15
        excel_stock_loc = {}
        for i in range(len(excel_stocks)):
            excel_stock_loc[curr_row] = excel_stocks[i]
            curr_row += 1

        output_summary = []
        for key, value in excel_stock_loc.items():
            price_new = round(products[value], 2)
            ws['J{}'.format(key)].value = price_new

            price_old = round(dict_old_value[value], 2)

            percentage_change = round(((price_new - price_old)/price_old)*100, 2)
            if percentage_change > 0:
                percentage_change = '+{}'.format(percentage_change)

            output_summary.append('{}: {} --> {} ({}%)'.format(value, price_old, price_new, percentage_change))
        #
        if save:
            wb.save(self.portfolio_path)    # In order to make changes have effect, put save = True
            print('Success! The new stock values were saved to {}\n\nThe following changes were made:\n'.format(
                self.portfolio_path))
        else:
            print('Success! The results were not saved. If you want to save the results, add save=True to update_stocks().'
                  '\n\nThe following changes were made:'.format(self.portfolio_path))

        for summary in output_summary:
            print(summary)

        print('\n')


class CryptoUpdateCSV:
    def __init__(self):
        self.portfolio_path = os.getenv("PORTFOLIO_CSV")

    def get_excel_coins(self):
        coins_portfolio = pd.read_excel(self.portfolio_path, sheet_name='Crypto portfolio', header=9, usecols="A:E",
                                        nrows=17)

        excel_coins = list(coins_portfolio["Code"])
        coins_value_old = list(coins_portfolio["Huidige waarde"])
        dict_old_coin_value = dict(zip(excel_coins, coins_value_old))
        dict_old_coin_value = {k: v for k, v in dict_old_coin_value.items() if v != 0}
        coins = list(dict_old_coin_value.keys())
        excel_coins = [x for x in excel_coins if x in coins]
        return excel_coins, dict_old_coin_value

    def update_coins(self, excel_coins, dict_old_value, bitv_port, bin_port, save=False):
        wb = pyxl.load_workbook(filename=self.portfolio_path)
        ws = wb.worksheets[1]

        crypto_portfolio = {}
        for d in (bitv_port, bin_port):
            for k, v in d.items():
                if v != 0.0:
                    if k in crypto_portfolio:
                        crypto_portfolio[k] += v
                    else:
                        crypto_portfolio[k] = v

        excel_coins = [x for x in excel_coins if x in crypto_portfolio]
        crypto_portfolio = {k: v for k, v in crypto_portfolio.items() if k in excel_coins}

        curr_row = 11
        excel_stock_loc = {}
        for i in range(len(excel_coins)):
            excel_stock_loc[curr_row] = excel_coins[i]
            curr_row += 1

        output_summary = []
        for key, value in excel_stock_loc.items():
            price_new = round(crypto_portfolio[value], 2)
            ws['E{}'.format(key)].value = price_new

            price_old = round(dict_old_value[value], 2)

            percentage_change = round(((price_new - price_old)/price_old)*100, 2)
            if percentage_change > 0:
                percentage_change = '+{}'.format(percentage_change)

            output_summary.append('{}: {} --> {} ({}%)'.format(value, price_old, price_new, percentage_change))

        if save:
            wb.save(self.portfolio_path)    # In order to make changes have effect, put save = True
            print('Success! The new coin values were saved to {}\n\nThe following changes were made:\n'.format(self.portfolio_path))
        else:
            print('Success! The results were not saved. If you want to save the results, add save=True to update_stocks().'
                  '\n\nThe following changes were made:'.format(self.portfolio_path))

        for summary in output_summary:
            print(summary)

        print('\n')

