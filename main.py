from degiro_tracker import DegiroFunctions
from dotenv import load_dotenv
import os


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


def get_degiro_login():
    username = os.getenv("DEGIRO_USERNAME")
    password = os.getenv("DEGIRO_PASSWORD")

    return username, password


if __name__ == '__main__':
    load_dotenv()

    username, password = get_degiro_login()

    DGF = DegiroFunctions()     # Instantiate DGF object
    DGF.login(username, password)
    products = DGF.fetch_portfolio()


