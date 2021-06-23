import os
import pandas as pd
import openpyxl as pyxl
from degiro_tracker import DegiroFunctions


class DegiroUpdateCSV:
    def __init__(self):
        with open("len_products.txt", "r") as f:
            self.products = int(f.read())

        self.portfolio_path = os.getenv("PORTFOLIO_CSV")
        self.header_value = 15  # Start of stock portfolio rows (header)

    def get_excel_stocks(self):
        stocks_portfolio = pd.read_excel(self.portfolio_path, sheet_name='Stocks portfolio',
                                         header=self.header_value - 2, usecols="A:J",
                                         nrows=self.products - 1)

        excel_stocks = list(stocks_portfolio["Code"])

        return excel_stocks

    def update_stocks(self, excel_stocks, DGF):

        wb = pyxl.load_workbook(filename=self.portfolio_path)
        ws = wb.worksheets[0]

        stock_cells = []
        count = self.header_value
        for i in range(len(excel_stocks)):
            stock_cells.append('B{}'.format(count))
            count += 1

        products = DGF.fetch_portfolio()

        if not os.path.isfile("len_products.txt"):
            with open("len_products.txt", "w") as f:
                f.write(str(len(products)))
            f.close()

        for cell in stock_cells:
            print(ws[cell].value)
