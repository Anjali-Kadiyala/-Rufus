import requests
import os

class RufusClient:
    def __init__(self, api_key, base_url='http://127.0.0.1:5001'):
        """
        Initializes the Rufus client with an API key and base URL for the API.
        
        :param api_key: The API key to authenticate the client
        :param base_url: The base URL of the API (default is 127.0.0.1:5001)
        """
        self.api_key = api_key
        self.base_url = base_url

    def scraper_tool(self, url, prompt, max_depth=2):
        """
        Sends a POST request to the /scrape endpoint of the API.
        
        :param url: The URL to scrape
        :param prompt: The user's instructions 
        :param max_depth: Maximum depth for nested page scraping 
        :return: Scraped content as a dictionary or an error message
        """
        endpoint = f"{self.base_url}/scrape"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        payload = {
            'url': url,
            'prompt': prompt,
            'max_depth': max_depth
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()  
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return {"error": str(e)}