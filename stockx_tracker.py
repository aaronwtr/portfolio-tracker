import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd
from googlesearch import search
import pickle
from datetime import date
import numpy as np


class StockXFunctions:

    def __init__(self):
        self.website = 'https://stockx.com/portfolio'

        self.stockx_username = os.getenv('STOCKX_USERNAME')
        self.stockx_password = os.getenv('STOCKX_PASSWORD')

        self.portfolio_path = os.getenv("PORTFOLIO_CSV")
        self.header_value = 23
        self.num_items = 13

    def get_inventory(self):
        sneakers_inventory = pd.read_excel(self.portfolio_path, sheet_name='Sneakers portfolio',
                                           header=self.header_value - 2, usecols="A:F",
                                           nrows=self.num_items)

        items = sneakers_inventory["Inventaris"]

        return items

    def scrape_stockx(self, items):
        updated_items = []
        for item in items:
            if type(item) != float:
                updated_items.append(item)

        items = updated_items
        
        try:
            raw_prior_inventory_data = open("item_prices.pkl", "rb")
            prior_inventory_data = pickle.load(raw_prior_inventory_data)
        except (FileNotFoundError, EOFError):
            open("item_prices.pkl", "w")
            prior_inventory_data = {}

        count = 0

        for item in items:
            today = date.today()
            string_today = today.strftime("%d/%m/%Y")

            prior_items = list(prior_inventory_data.keys())

            if prior_items:
                if item in prior_items:
                    item_last_retrieved = prior_inventory_data[item][1]
                    if item_last_retrieved == string_today:
                        continue

            count += 1
            chrome_options = Options()
            chrome_options.add_argument("--enable-javascript")

            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            google_search = str(item) + ' StockX'

            print('\n\nScraping ' + str(item) + '...')

            item_price_data = []

            for result in search(google_search,  # The query you want to run
                                 lang='nl',  # The language
                                 num_results=0,  # Number of results per page
                                 ):

                link = result

                driver.get(link)

                time.sleep(0.1)
                driver.find_element_by_class_name('chakra-modal__close-btn.css-1iqbypn').click()

                time.sleep(0.1)

                driver.find_element_by_class_name('css-unzfas-button').click()

                time.sleep(0.1)

                driver.execute_script("window.scrollTo(0, 1000)")

                time.sleep(0.1)

                try:
                    driver.find_element_by_class_name('chakra-button.css-xk3212').click()
                except NoSuchElementException:
                    try:
                        driver.execute_script("window.scrollTo(0, 800)")
                        driver.find_element_by_xpath(
                            '//*[@id="main-content"]/div/section[4]/div/div/div/div/div[1]/div[2]/button').click()
                        time.sleep(0.1)
                    except ElementClickInterceptedException:
                        try:
                            driver.execute_script("window.scrollTo(0, 800)")
                            driver.find_element_by_xpath(
                                '//*[@id="root"]/div[1]/div[2]/div[2]/div[9]/div/div/div/div[2]/div/div[2]/div/button').click()
                            time.sleep(0.1)
                            driver.find_element_by_xpath(
                                '//*[@id="root"]/div[1]/div[2]/div[2]/div[9]/div/div/div/div[2]/div/div[1]/div[2]/button').click()
                        except ElementClickInterceptedException:
                            print('koekoek')
                            driver.execute_script("window.scrollTo(0, 300)")
                            driver.find_element_by_xpath(
                                '//*[@id="root"]/div[1]/div[2]/div[2]/div[9]/div/div/div/div[2]/div/div[2]/div/button').click()

                except ElementClickInterceptedException:
                    driver.execute_script("window.scrollTo(0, 800)")
                    driver.find_element_by_xpath('//*[@id ="root"]/div[1]/div[2]/div[2]/div[9]/div/div/div/div[2]/div/div[2]/ \
                                                                            div/button').click()

                try:
                    driver.find_element_by_xpath(
                        '//*[@id="root"]/div[1]/div[2]/div[2]/div[2]/section/div/div/div/div[1]/div[2]/button').click()
                except (ElementClickInterceptedException, NoSuchElementException):
                    pass

                time.sleep(1)
                item_table = driver.find_elements_by_class_name('css-1ki54i')
                if len(item_table) == 0:
                    item_table = driver.find_elements_by_class_name(
                        'activity-table.table.table-condensed.table-striped')

                raw_data = []
                try:
                    for i in item_table:
                        raw_data = str(i.text).split(sep='\n')

                    last_sales = []
                    for data in raw_data:
                        if '\u20AC' in data and len(last_sales) != 10:
                            last_sales.append(int(data[1:]))

                except ValueError:
                    for i in item_table:
                        raw_data = str(i.text).split(sep=' ')

                    last_sales = []

                    for data in raw_data:
                        data = data.split('\n')
                        if len(data) != 0:
                            if '\u20AC' in data[0] and len(last_sales) != 10:
                                last_sales.append(int(data[0][1:]))

                try:
                    avg_price = sum(last_sales) / len(last_sales)
                    item_price_data.append(round(avg_price, 2))
                except ZeroDivisionError:
                    item_price_data.append("Look up price manually!")

                item_price_data.append(string_today)

                item_price_temp = {item: item_price_data}

                item_prices = prior_inventory_data
                item_prices.update(item_price_temp)

                print(str(item_price_data) + " is added to the datafile!")
                save_item_prices = open("item_prices.pkl", "rb+")
                pickle.dump(item_prices, save_item_prices)
                save_item_prices.close()

                driver.close()
                driver.quit()

        return
