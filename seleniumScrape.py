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
    # pick a random user agent
    user_agent = random.choice(user_agent_list)
    # set the headers
    headers = {'User-Agent' : user_agent}
    result = requests.get(f"https://www.diy.com/departments/flooring-tiling/flooring-underlay/laminate-flooring/DIY566433.cat?page={x}", headers=headers)

# response status
print(result.status_code)

# enable driver
path = "/Applications/chromedriver"
chrome_options = Options()
chrome_options.add_argument(" - incognito")
driver = webdriver.Chrome(path, options=chrome_options)

productInfo = []

for x in range(1,6):
    # select url link
    url = "https://www.diy.com/departments/flooring-tiling/flooring-underlay/laminate-flooring/DIY566433.cat?page="
    driver.get(url+str(x))

    try:
        # accept cookies
        WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@title="TrustArc Cookie Consent Manager"]')))
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='call'][text()='Accept Cookies']"))).click()

        driver.switch_to.default_content()
    except:
        break
    
    time.sleep(5)

    # baseurl = 'https://www.diy.com/'

def scrape():
    flooring = driver.find_elements_by_css_selector('.b9bdc658')

    # get product info
    for f in flooring:
        title = f.find_element_by_css_selector('p').text
        testLink = f.find_elements_by_tag_name('a')
        l = []
        for link in testLink:
            l.append(link.get_attribute('href'))
        """ link = f.find_elements_by_tag_name('a')
        for l in link:
            products.append(l.get_attribute('href'))"""
        price = f.find_element_by_xpath('.//div[@class="b25ad5d5 _4e80f7be _23ee746f _7b343263"]').text
        unitPrice = f.find_element_by_xpath('.//div[@class="b00398fe b1bfb616"]').text
        rating = f.find_element_by_xpath('.//div[@class="_45e852d0 _6418d197 _2263bdd0"]').text
        reviewNum = f.find_element_by_xpath('.//span[@class="ccb9d67a _17d3fa36 _50344329 b1bfb616 cc6bbaee"]').text

        products = {
            'title': title,
            # 'testLink': testLink,
            'link': l,
            'price': price,
            'unitPrice': unitPrice,
            'rating': rating,
            'reviewNum': reviewNum
        }

        productInfo.append(products)

# call scrape function
scrape()

# return length of results
print(len(productInfo))

# close browser
driver.close()

# create dataframe
df = pd.DataFrame(productInfo)
pd.set_option('display.max_columns', 100)

# save to excel
df.to_excel('floor_lights.xlsx', index=True, header=True)
data = pd.read_excel('/Users/jforbes84/PycharmProjects/floor_lights.xlsx')
print(data)
