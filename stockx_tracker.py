import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd
from googlesearch import search
import openpyxl as pyxl
from lxml import html


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

        items = list(sneakers_inventory["Inventaris"])

        return items

    def scrape_stockx(self, items):
        chrome_options = Options()
        chrome_options.add_argument("--enable-javascript")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        for item in items:
            google_search = str(item) + 'StockX'

            print('\n\nScraping ' + str(item) + '...')

            for result in search(google_search,  # The query you want to run
                                 lang='en',  # The language
                                 num_results=1,  # Number of results per page
                                 ):
                link = result

                driver.get(link)

                time.sleep(1)

                driver.find_element_by_class_name('chakra-modal__close-btn.css-17sthuj').click()

                time.sleep(1)

                driver.find_element_by_class_name('css-unzfas-button').click()

                time.sleep(1)

                driver.execute_script("window.scrollTo(0, 1000)")

                time.sleep(1)

                try:
                    driver.find_element_by_class_name('chakra-button.css-xk3212').click()
                except NoSuchElementException:
                    driver.find_element_by_xpath(
                        '//*[@id="root"]/div[1]/div[2]/div[2]/div[9]/div/div/div/div[2]/div/div[1]/div[2]/button').click()
                except ElementClickInterceptedException:
                    driver.execute_script("window.scrollTo(0, 800)")
                    driver.find_element_by_xpath('//*[ @ id = "root"]/div[1]/div[2]/div[2]/div[9]/div/div/div/div[2]/div/div[1]/ \
                                           div[2]/button').click()

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

                    print(last_sales)

                except ValueError:
                    for i in item_table:
                        raw_data = str(i.text).split(sep=' ')

                    last_sales = []

                    for data in raw_data:
                        data = data.split('\n')
                        if len(data) != 0:
                            if '\u20AC' in data[0] and len(last_sales) != 10:
                                last_sales.append(int(data[0][1:]))

                    print(last_sales)

                # CALCULATE AVERAGE

                while True:
                    time.sleep(0.1)

                driver.quit()

        return
