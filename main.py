from typing import List, Any
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# import random
# import lxml

# http://myhttpheader.com/ don't forget to pass all the headers

FORM_LINK_ADDRESS = 'https://docs.google.com/forms/d/e/1FAIpQLSdEjg5ht0G_q_lKBgIFXyT9arF9JnLdkijaaYuCtAzm1oruZg/viewform?usp=sf_link'
SPREADSHEET_ADDRESS = 'https://docs.google.com/spreadsheets/d/1wnofMHndAIqUmxs_111QlFkvFlYa2K4iGYNGJgKDlQc/edit?resourcekey#gid=769645818'
ZILLOW_PAGE = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'
CHROME_DRIVER_PATH = webdriver.ChromeOptions()
CHROME_DRIVER_PATH.add_experimental_option('detach', True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "upgrade-insecure-requests": "1",
    "sec-fetch-site": "cross-site",
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(ZILLOW_PAGE, headers=headers)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

listing_hrefs = soup.find_all(name='a', class_='property-card-link')
listing_links = []
for tag in listing_hrefs:
    new_item = tag.get('href')
    if new_item.find('https://www.zillow.com') == -1:
        new_item = 'https://www.zillow.com' + new_item
    listing_links.append(new_item)
    listing_links = list(dict.fromkeys(listing_links))

listing_price_data = soup.find_all(class_='PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr')
listing_prices: list[Any] = []
for price in listing_price_data:
    listing_prices.append(price.string[:6])

address_data = soup.find_all(name='address')
addresses = []
for address in address_data:
    addresses.append(address.string)


class FormFillerBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(options=driver_path)
        self.driver.get(FORM_LINK_ADDRESS)
        time.sleep(2)

    def fill_form(self, link, pricefill, addressfill):
        loc_link = self.driver.find_element(By.CSS_SELECTOR,
                                            value='#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
        loc_link.send_keys(f'{link}')
        loc_price = self.driver.find_element(By.CSS_SELECTOR,
                                             value='#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(2) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
        loc_price.send_keys(f'{pricefill}')
        loc_add = self.driver.find_element(By.CSS_SELECTOR,
                                           value='#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(3) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
        loc_add.send_keys(f'{addressfill}')
        submit = self.driver.find_element(By.CSS_SELECTOR,
                                          value='#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > div.lRwqcd > div > span > span')
        submit.click()
        another = self.driver.find_element(By.CSS_SELECTOR, value='body > div.Uc2NEf > div:nth-child(2) > div.RH5hzf.RLS9Fe > div > div.c2gzEf > a')
        another.click()

    def quit(self):
        self.driver.quit()


bot = FormFillerBot(CHROME_DRIVER_PATH)
for i in range(len(listing_links) - 1):
    bot.fill_form(listing_links[i], listing_prices[i], addresses[i])
bot.quit()

