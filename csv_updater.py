import os
import pandas as pd
import openpyxl as pyxl


class DegiroUpdateCSV:
    def __init__(self):
        with open("len_products.txt", "r") as f:
            self.products = int(f.read())

        self.portfolio_path = os.getenv("PORTFOLIO_CSV")
        self.header_value = 15  # Start of stock portfolio rows

    def get_excel_stocks(self):
        stocks_portfolio = pd.read_excel(self.portfolio_path, sheet_name='Stocks portfolio',
                                         header=self.header_value - 2, usecols="A:J",
                                         nrows=self.products - 1)

        excel_stocks = list(stocks_portfolio["Code"])
        stocks_value_old = list(stocks_portfolio["Huidige waarde"])

        dict_old_value = dict(zip(excel_stocks, stocks_value_old))

        return excel_stocks, dict_old_value

    def update_stocks(self, excel_stocks, dict_old_value, DGF, save=False):

        wb = pyxl.load_workbook(filename=self.portfolio_path)
        ws = wb.worksheets[0]

        products = DGF.fetch_portfolio()

        if not os.path.isfile("len_products.txt"):
            with open("len_products.txt", "w") as f:
                f.write(str(len(products)))
            f.close()

        count = self.header_value
        excel_stock_loc = {}
        for i in range(len(excel_stocks)):
            excel_stock_loc[count] = excel_stocks[i]
            count += 1

        output_summary = []
        for key, value in excel_stock_loc.items():
            price_new = round(products[value], 2)
            ws['J{}'.format(key)].value = price_new

            price_old = round(dict_old_value[value], 2)
            output_summary.append('{}: {} --> {}'.format(value, price_old, price_new))

        if save:
            wb.save(self.portfolio_path)    # In order to make changes have effect, put save = True
            print('Success! The results were saved to {}\n\nThe following changes were made:\n'.format(
                self.portfolio_path))
        else:
            print('Success! The results were not saved. If you want to save the results, add save=True to update_stocks().'
                  '\n\nThe following changes were made:'.format(self.portfolio_path))

        for summary in output_summary:
            print(summary)

        print('\n')

