# rufus/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def setup_driver():
    options = Options()
    options.add_argument('--headless')  # Headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    service = Service('/usr/local/bin/chromedriver')  # Update with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)  # Set a timeout for the page load
    return driver

def collect_links(soup, base_url, max_links=5):
    """
    Collects all internal links from a webpage.
    
    :param soup: BeautifulSoup object of the page
    :param base_url: The base URL of the page
    :return: List of internal URLs found on the page
    """
    links = []
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        # Filter to avoid external links or non-relevant links (e.g., based on patterns or keywords)
        if full_url.startswith(base_url) and len(links) < max_links:  # Ensure we stay within the same domain
            links.append(full_url)
    return links


def scrape_elements(url, elements, depth=1, max_depth=2):
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

        # If depth allows, scrape nested pages
    if depth < max_depth:
        nested_links = collect_links(soup, url)
        nested_data = {}
        for link in nested_links:
            try:
                nested_content = scrape_elements(link, elements, depth + 1, max_depth)
                nested_data[link] = nested_content
            except Exception as e:
                print(f"Error scraping {link}: {e}")
        
        scraped_data['nested_pages'] = nested_data


    return scraped_data