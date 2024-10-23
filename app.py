from flask import Flask, request, jsonify
import logging
from element_collector import collect_elements
from llm_integration import ask_chatgpt
from response_parser import parse_chatgpt_response
from scraper import scrape_elements
import os
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

def clean_scraped_content(content):
    """
    Removes duplicates from the scraped content.
    
    :param content: The dictionary containing the scraped content
    :return: A cleaned dictionary with duplicates removed
    """
    cleaned_content = {}
    for key, values in content.items():
        if isinstance(values, list):
            # Remove duplicates from lists
            cleaned_content[key] = list(set(values))
        elif isinstance(values, dict):
            # Recursively clean nested dictionaries
            cleaned_content[key] = clean_scraped_content(values)
        else:
            cleaned_content[key] = values
    return cleaned_content


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        logging.debug("Received a POST request to /scrape")

        # Get JSON data from the request
        data = request.get_json()
        url = data.get('url')
        user_prompt = data.get('prompt')
        max_depth = data.get('max_depth', 2)  # Default max depth is 2

        # Validate input
        if not url or not user_prompt:
            logging.error("Missing 'url' or 'prompt' in request")
            return jsonify({"error": "Both 'url' and 'prompt' fields are required."}), 400

        # Collect elements from the webpage
        logging.debug("Collecting elements from the webpage")
        elements = collect_elements(url)

        # Make a ChatGPT API call to determine relevant elements
        logging.debug("Calling ChatGPT API with collected elements")
        chatgpt_response = ask_chatgpt(elements, user_prompt)

        # Parse ChatGPT's response to get tags, classes, and ids
        logging.debug("Parsing ChatGPT response")
        parsed_elements = parse_chatgpt_response(chatgpt_response)

        # Scrape the webpage based on the parsed elements and nested pages
        logging.debug("Scraping elements from the webpage")
        scraped_content = scrape_elements(url, parsed_elements, max_depth=max_depth)

        # Remove duplicates from scraped content
        cleaned_content = clean_scraped_content(scraped_content)

        # Save the cleaned content as a JSON file in the current working directory
        file_path = os.path.join(os.getcwd(), 'scraped_content.json')
        with open(file_path, 'w') as json_file:
            json.dump(cleaned_content, json_file, indent=4)
        logging.debug(f"Scraped content saved as JSON at: {file_path}")


        # Return the cleaned content as JSON
        logging.debug("Returning cleaned scraped content as JSON")
        return jsonify({"scraped_content": cleaned_content})

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logging.debug("Starting the Flask app")
    app.run(host='0.0.0.0', port=5001, debug=True)