# rufus/data_extractor.py

from bs4 import BeautifulSoup
import json

def extract_content(soup, tags):
    """
    Extracts specific content based on the HTML tags provided.
    
    :param soup: BeautifulSoup object containing the page source
    :param tags: List of HTML tags or CSS classes/IDs to extract data from (e.g., 'div', 'p', 'span')
    :return: List of extracted content blocks as strings
    """
    content_blocks = []
    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            text = element.get_text(strip=True)
            if text:  # Add a check to filter out empty strings
                content_blocks.append(text)
    return content_blocks

def clean_data(content_blocks):
    """
    Cleans the extracted data by removing duplicates, irrelevant entries, and filtering out certain patterns.
    
    :param content_blocks: List of extracted content strings
    :return: Cleaned list of content
    """
    cleaned_blocks = []
    seen_blocks = set()
    for block in content_blocks:
        # Filter out common repetitive elements or irrelevant phrases (like 'Original text', 'Powered by')
        if block not in seen_blocks and not block.lower().startswith(('powered by', 'original text', 'select language')):
            seen_blocks.add(block)
            cleaned_blocks.append(block)
    return cleaned_blocks

def structure_data(content_blocks, output_format='json'):
    """
    Structures the extracted data into a chosen format.
    
    :param content_blocks: List of extracted content strings
    :param output_format: Format of the output ('json' or 'csv')
    :return: Structured data in the chosen format
    """
    cleaned_content = clean_data(content_blocks)
    if output_format == 'json':
        data = {"content": cleaned_content}
        return json.dumps(data, indent=4)
    # Add other formats (e.g., CSV) if needed
    return cleaned_content

def extract_and_structure(soup, tags, output_format='json'):
    """
    Combines extraction and structuring into a single function.
    
    :param soup: BeautifulSoup object containing the page source
    :param tags: List of tags to look for (e.g., 'p', 'div')
    :param output_format: Format to return ('json' or 'plain')
    :return: Data structured as JSON or plain text
    """
    content = extract_content(soup, tags)
    structured_data = structure_data(content, output_format)
    return structured_data
