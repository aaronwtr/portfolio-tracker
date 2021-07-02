import degiroapi
import os

class DegiroFunctions:

    def __init__(self):
        self.degiro = degiroapi.DeGiro()

    def get_degiro_login(self):
        username = os.getenv("DEGIRO_USERNAME")
        password = os.getenv("DEGIRO_PASSWORD")

        return username, password

    def login(self, username, password):
        self.degiro.login(username, password)

    def logout(self):
        self.degiro.logout()

    def fetch_portfolio(self):
        print('Fetching data from DeGiro API...\n')
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
