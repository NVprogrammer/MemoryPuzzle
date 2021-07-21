import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
import re
import wget
from PIL import Image
import os
def get_browser_images():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    browser=webdriver.Chrome("D:/chromedriver.exe",chrome_options=chrome_options)

    # get source code
    browser.get("https://ru.depositphotos.com/stock-photos/jpg.html")
    urls=[]
    images = browser.find_elements_by_tag_name('img')
    for i,image in enumerate(images):
        urls.append(image.get_attribute('src'))
        if i==50:break
    print(urls)
    for i,j in enumerate(urls):
        wget.download(j, f'images/{i}.jpg')


