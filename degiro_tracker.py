import degiroapi
from degiroapi.product import Product
from degiroapi.order import Order
from degiroapi.utils import pretty_json


class DegiroFunctions:

    def __init__(self):
        self.degiro = degiroapi.DeGiro()

    def login(self, username, password):
        self.degiro.login(username, password)

    def logout(self):
        self.degiro.logout()

    def fetch_portfolio(self):
        portfolio = self.degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)
        products = []

        for data in portfolio:
            products.append(data)

        product_and_value = {}
        for product in products:
            prod_id = product['id']
            prod_value = product['value']
            prod_info = self.degiro.product_info(prod_id)
            prod_name = prod_info['symbol']

            product_and_value[prod_name] = prod_value

        return product_and_value
