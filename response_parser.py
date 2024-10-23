import json

def parse_chatgpt_response(response):
    """
    Parses ChatGPT's response to extract the relevant elements (tags, classes, IDs).
    
    :param response: The string response from ChatGPT.
    :return: A dictionary with tags, classes, and ids to be scraped.
    """
    try:
        start_index = response.find('{')
        end_index = response.rfind('}') + 1
        
        if start_index == -1 or end_index == -1:
            raise ValueError("Response does not contain a valid JSON-like format.")
        
        json_part = response[start_index:end_index]
        parsed_response = json.loads(json_part)
        
        tags = parsed_response.get('tags', [])
        classes = parsed_response.get('classes', [])
        ids = parsed_response.get('ids', [])
        
        return {'tags': tags, 'classes': classes, 'ids': ids}
    except (json.JSONDecodeError, ValueError) as e:
        print("An error occurred while parsing the response:", e)
        return {'tags': [], 'classes': [], 'ids': []}
