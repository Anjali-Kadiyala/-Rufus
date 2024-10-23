from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def ask_chatgpt(elements, user_prompt):
    """
    Calls the ChatGPT API with the extracted elements and the user prompt to determine relevant elements to scrape.
    
    :param elements: List of extracted elements (tags, classes, ids)
    :param user_prompt: The input prompt provided by the user
    :return: Response from ChatGPT
    """
    elements_str = json.dumps(elements, indent=2)
    # print('element_len:', len(elements_str))
    # print('elements:', elements_str)

    prompt = f"""
    Here is the structure of a webpage with elements represented as JSON:
    {elements_str}
    
    Based on the user prompt: '{user_prompt}', which elements (tags, classes, ids) are most likely to contain the relevant information?
    Please provide a list of element keys (tags, classes, ids) that are most appropriate for scraping the information relevant to the prompt. Format your response in the following structured format as the last line:
    {{
        "tags": ["tag1", "tag2", ...],
        "classes": ["class1", "class2", ...],
        "ids": ["id1", "id2", ...]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an assistant specialized in web scraping."},
                      {"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None