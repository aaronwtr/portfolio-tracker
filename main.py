from degiro_tracker import DegiroFunctions
from csv_updater import DegiroUpdateCSV
from crypto_tracker import BinanceFunctions
from crypto_tracker import BitvavoFunctions
from stockx_tracker import StockXFunctions
from dotenv import load_dotenv
import pickle


"""
    Portfolio Tracker
    Copyright (C) 2021  Aaron Wenteler

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


if __name__ == '__main__':
    load_dotenv()

    """
        Importing data from DeGiro API and updating the specified Excel file with the gathered data.
    """

    # DGF = DegiroFunctions()  # Instantiate DGF object
    # username, password = DGF.get_degiro_login()
    # DGF.login(username, password)
    #
    # UpdateCSVGiro = DegiroUpdateCSV()
    # excel_stocks, dict_old_value = UpdateCSVGiro.get_excel_stocks()
    # UpdateCSVGiro.update_stocks(excel_stocks, dict_old_value, DGF, save=False)
    #
    # DGF.logout()

    """
        Importing data from Binance API and Bitvavo API and updating the specified Excel file with the gathered data.
    """

    # BF = BinanceFunctions()
    # binance_portfolio = BF.get_balances()
    # print(binance_portfolio)
    #
    # BV = BitvavoFunctions()
    # bitvavo_portfolio = BV.get_balances()
    # print(bitvavo_portfolio)

    """
        Scraping StockX, logging in and fetching portfolio. Then, the price is calculated based on the previous 10 sales
        for that particular item.
    """

    StockX = StockXFunctions()
    inventory = StockX.get_inventory()

    StockX.scrape_stockx(inventory)     # This function creates a .pkl file that is externally so multiple runs can be
                                        # performed in the case of discontinuations.

    StockXOutput = open("item_prices.pkl", "rb")
    stockx_prices = pickle.load(StockXOutput)
    print(stockx_prices)
