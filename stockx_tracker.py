import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os


class StockXFunctions:

    def __init__(self):
        self.website = 'https://stockx.com/portfolio'

        self.stockx_username = os.getenv('STOCKX_USERNAME')
        self.stockx_password = os.getenv('STOCKX_PASSWORD')

    def scrape_stockx(self):
        chrome_options = Options()

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        driver.get(self.website)
        time.sleep(1)

        driver.find_element_by_xpath('//*[@id="login-toggle"]').click()

        username = driver.find_element_by_xpath('//*[@id="email-login"]')
        username.send_keys(self.stockx_username)
        username.send_keys(Keys.ENTER)

        password = driver.find_element_by_xpath('//*[@id="password-login"]')
        password.send_keys(self.stockx_password)
        password.send_keys(Keys.ENTER)

        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="chakra-modal-3"]/footer/button').click()

        time.sleep(1)

        driver.refresh()

        while True:
            time.sleep(0.1)

        driver.quit()

        return
