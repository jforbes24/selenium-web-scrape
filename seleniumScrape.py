import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import lxml
import random
import numpy as np
import pandas as pd
import time

# assign user-agent
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    ]

for x in range(1,6):
    for i in range(1,6):
        # pick a random user agent
        user_agent = random.choice(user_agent_list)
        # set the headers
        headers = {'User-Agent' : user_agent}
        result = requests.get(f"https://www.diy.com/departments/lighting/indoor-lights/floor-lamps/DIY579453.cat?page={x}", headers=headers)

# response status
print(result.status_code)

# enable driver
path = "/Applications/chromedriver"
chrome_options = Options()
chrome_options.add_argument(" - incognito")
driver = webdriver.Chrome(path, options=chrome_options)

# select url link
url = "https://www.diy.com/departments/lighting/indoor-lights/floor-lamps/DIY579453.cat?"
driver.get(url)

# accept cookies
WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@title="TrustArc Cookie Consent Manager"]')))
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='call'][text()='Accept Cookies']"))).click()

driver.switch_to.default_content()

time.sleep(5)

products = [] # list to store name of the product
links = [] # list to store link of the product
prices = [] # list to store price of the product
ratings = [] # list to store rating of the product
# baseurl = 'https://www.diy.com/'


lights = driver.find_elements_by_css_selector('.b9bdc658')


# get product info
for i in lights:
    title = i.find_element_by_css_selector('p').text
    link = i.find_elements_by_tag_name('a')
    for l in link:
        links.append(l.get_attribute('href'))
    # price = i.find_element_by_css_selector('div.b25ad5d5 _4e80f7be _23ee746f _7b343263 > span').text
    products.append(title)
    # prices.append(price)
print(products, links, prices)

# driver.find_element_by_css_selector("div.pv-entity__summary-info > h3").text
# driver.find_element_by_css_selector("div.pv-entity__summary-info span.pv-entity__secondary-title").text

"""

# get top lvl product view
for light in lights:
    products = light.find_elements_by_class_name('li')
    price = light.find_element_by_xpath('.//*[@id="content"]/div/div[1]/div/div/div[3]/div/div[3]/div[2]/main/div/ul/li[1]/div/a/div[2]/div/div[2]/div/div[2]/div/span[2]').text
    print(price)
"""
driver.close()    



