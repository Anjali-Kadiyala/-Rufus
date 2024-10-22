# rufus/agent.py

from web_crawler import crawl_page
from data_extractor import extract_and_structure

class RufusAgent:
    def __init__(self):
        pass

    def run(self, url, tags=['p', 'div']):
        """
        Run the Rufus agent to crawl and extract content based on tags.
        
        :param url: The URL to crawl
        :param tags: List of HTML tags to look for
        :return: Structured data in JSON format
        """
        # Crawl the page to get the soup object
        soup = crawl_page(url)
        
        # Extract and structure the data
        structured_data = extract_and_structure(soup, tags)
        return structured_data

# # Example usage
# if __name__ == "__main__":
#     agent = RufusAgent()
#     result = agent.run("https://sf.gov", tags=['h1', 'h2', 'p', 'div'])
#     print(result)

