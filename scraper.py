# rufus/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def setup_driver():
    options = Options()
    options.add_argument('--headless')  # Headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    service = Service('/usr/local/bin/chromedriver')  # Update with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_elements(url, elements):
    """
    Scrapes elements from a webpage based on the tags, classes, and ids provided.
    
    :param url: URL of the webpage to scrape
    :param elements: A dictionary containing 'tags', 'classes', and 'ids'
    :return: A dictionary with the scraped content
    """
    driver = setup_driver()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    scraped_data = {}

    # Scrape by tags
    for tag in elements['tags']:
        tag_elements = soup.find_all(tag)
        scraped_data[tag] = [element.get_text(strip=True) for element in tag_elements]

    # Scrape by classes
    for class_name in elements['classes']:
        class_elements = soup.find_all(class_=class_name)
        scraped_data[f'class:{class_name}'] = [element.get_text(strip=True) for element in class_elements]

    # Scrape by ids
    for id_name in elements['ids']:
        id_element = soup.find(id=id_name)
        if id_element:
            scraped_data[f'id:{id_name}'] = id_element.get_text(strip=True)

    return scraped_data
