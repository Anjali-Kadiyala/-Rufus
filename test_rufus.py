
from client import RufusClient
import os

def main():

    key = os.getenv('Rufus_API_KEY')

    client = RufusClient(api_key=key)

    url = "https://wwww.sjsu.edu"  # Replace with a real website
    prompt = "Scrape news from the SJSU website"
    max_depth = 2

    # Make the API call
    result = client.scraper_tool(url, prompt, max_depth=max_depth)

    # Print the result
    if "error" not in result:
        print("Scraped Content:", result['scraped_content'])
    else:
        print("Error:", result["error"])

if __name__ == "__main__":
    main()
