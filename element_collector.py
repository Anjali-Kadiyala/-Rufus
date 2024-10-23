# rufus/element_collector.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def setup_driver():
    options = Options()
    options.add_argument('--headless') 
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    service = Service('/usr/local/bin/chromedriver') 
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def collect_elements(url):
    driver = setup_driver()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    elements = []
    for tag in soup.find_all(True):  
        element = {
            'tag': tag.name,
            'class': tag.get('class'),
            'id': tag.get('id'),
            'text': tag.get_text(strip=True)[:50]  # Get a snippet of the text (first 50 characters)
        }


        if None not in (element['tag'], element['class'], element['id']):
            elements.append(element)
    
    return elements
