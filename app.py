from flask import Flask, request, jsonify
from element_collector import collect_elements
from llm_integration import ask_chatgpt
from response_parser import parse_chatgpt_response
from scraper import scrape_elements

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        # Get JSON data from the request
        data = request.get_json()
        url = data.get('url')
        user_prompt = data.get('prompt')

        # Validate input
        if not url or not user_prompt:
            return jsonify({"error": "Both 'url' and 'prompt' fields are required."}), 400

        # Step 1: Collect elements from the webpage
        elements = collect_elements(url)

        # Step 2: Make a ChatGPT API call to determine relevant elements
        chatgpt_response = ask_chatgpt(elements, user_prompt)

        # Step 3: Parse ChatGPT's response to get tags, classes, and ids
        parsed_elements = parse_chatgpt_response(chatgpt_response)

        # Step 4: Scrape the webpage based on the parsed elements
        scraped_content = scrape_elements(url, parsed_elements)

        # Return the scraped content as JSON
        return jsonify({"scraped_content": scraped_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
