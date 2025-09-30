from degiro_connector.trading.api import API
from degiro_connector.trading.models.trading_pb2 import (
    Credentials,
    Update,
    ProductsInfo
)
import os


class DegiroFunctions:

    def __init__(self):
        self.trading_api = None
        self.int_account = None

    def get_degiro_login(self):
        username = os.getenv("DEGIRO_USERNAME")
        password = os.getenv("DEGIRO_PASSWORD")
        # Optional: store TOTP secret key in env for automatic 2FA
        totp_secret = os.getenv("DEGIRO_TOTP_SECRET", None)

        return username, password, totp_secret

    def login(self, username, password, totp=None):
        """
        Login to Degiro.

        Args:
            username: Degiro username
            password: Degiro password
            totp: Either totp_secret_key (32 char string) or one_time_password (6 digit code)
        """
        # Create credentials object
        credentials = Credentials()
        credentials.username = username
        credentials.password = password

        # Handle 2FA if provided
        if totp:
            # If it's a 32-character string, treat it as totp_secret_key
            if len(totp) == 32 and totp.isalnum():
                credentials.totp_secret_key = totp
            # If it's 6 digits, treat it as one_time_password
            elif len(totp) == 6 and totp.isdigit():
                credentials.one_time_password = int(totp)
            else:
                credentials.totp_secret_key = totp

        self.trading_api = API(credentials=credentials)
        self.trading_api.connect()

        # Get int_account and set it in credentials
        client_details = self.trading_api.get_client_details()
        self.int_account = client_details['data']['intAccount']

        # Update credentials with int_account
        credentials.int_account = self.int_account

    def logout(self):
        if self.trading_api:
            self.trading_api.logout()

    def fetch_portfolio(self):
        from google.protobuf.json_format import MessageToDict

        print('Fetching data from DeGiro API...\n')

        # Create the request list container
        request_list = Update.RequestList()

        # Create and add the portfolio request
        portfolio_request = request_list.values.add()
        portfolio_request.option = Update.Option.PORTFOLIO
        portfolio_request.last_updated = 0

        # Fetch portfolio data - use raw=False to get protobuf
        portfolio_update = self.trading_api.get_update(
            request_list=request_list,
            raw=False,  # Get protobuf object
        )


        # Convert protobuf to dict
        portfolio_dict = MessageToDict(portfolio_update)

        print(f"Portfolio dict keys: {portfolio_dict.keys()}")

        portfolio_data = portfolio_dict.get('portfolio', {}).get('values', [])

        print(f"Portfolio data length: {len(portfolio_data)}")

        if not portfolio_data:
            print("Portfolio is empty")
            return {}

        # Filter out cash positions and get only actual product IDs
        product_ids = []
        for item in portfolio_data:
            item_id = item['id']
            position_type = item.get('positionType')
            prod_value = item.get('value', 0)

            # Only include products with non-zero values (skip sold positions and cash)
            if position_type == 'PRODUCT' and prod_value > 0:
                product_ids.append(int(item_id))

        print(f"Found {len(product_ids)} actual products with value: {product_ids}")

        if not product_ids:
            print("No products found (only cash positions)")
            return {}

        # Fetch product information - note: first positional argument, not keyword
        products_request = ProductsInfo.Request()
        products_request.products.extend(product_ids)

        # Fetch product information
        products_info = self.trading_api.get_products_info(
            request=products_request,
            raw=True,
        )

        print(f"Products info response: {products_info}")

        # Build the product_and_value dictionary
        product_and_value = {}

        for item in portfolio_data:
            prod_id = item['id']
            prod_value = item['value']
            position_type = item.get('positionType')

            # Only process products with value
            if position_type == 'PRODUCT' and prod_value > 0:
                if str(prod_id) in products_info['data']:
                    prod_info = products_info['data'][str(prod_id)]
                    prod_name = prod_info.get('symbol', prod_info.get('name', f'UNKNOWN_{prod_id}'))
                    product_and_value[prod_name] = prod_value

        with open('len_products.txt', 'w') as f:
            f.write(str(len(product_and_value)))

        return product_and_value