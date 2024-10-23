from element_collector import collect_elements
from llm_integration import ask_chatgpt
from response_parser import parse_chatgpt_response
from scraper import scrape_elements

def main(url, user_prompt):

    elements = collect_elements(url)
    chatgpt_response = ask_chatgpt(elements, user_prompt)
    print("ChatGPT Response:")
    print(chatgpt_response)

    parsed_elements = parse_chatgpt_response(chatgpt_response)
    print("Parsed elements to scrape:")
    print(parsed_elements)

    scraped_content = scrape_elements(url, parsed_elements, max_depth=2)
    print("Scraped Content:")
    print(scraped_content)

# Example usage
if __name__ == "__main__":
    url = "https://www.sf.gov/"
    user_prompt = "scrape the news from the SF website"
    main(url, user_prompt)
