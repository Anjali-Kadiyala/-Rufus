# rufus/web_crawler.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def setup_driver():
    # Configure Chrome options for headless mode (no browser window pops up)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service('/usr/local/bin/chromedriver')  # Update with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def crawl_page(url):
    driver = setup_driver()
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup
    finally:
        driver.quit()
