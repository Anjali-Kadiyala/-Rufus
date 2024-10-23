# rufus/document_synthesizer.py

import json

def synthesize_document(content, format='json'):
    """
    Synthesizes the extracted content into a structured document.
    
    :param content: The extracted and filtered content from the website
    :param format: The format in which to return the document ('json' or 'text')
    :return: The document in the specified format
    """
    if format == 'json':
        return synthesize_json(content)
    elif format == 'text':
        return synthesize_text(content)
    else:
        raise ValueError("Unsupported format. Use 'json' or 'text'.")

def synthesize_json(content):
    """
    Converts the extracted content into a JSON format.
    
    :param content: The extracted content
    :return: JSON representation of the content
    """
    try:
        # Ensure the content is structured properly for JSON format
        structured_data = {
            "headings": content.get('h1', []) + content.get('h2', []) + content.get('h3', []),
            "paragraphs": content.get('p', []),
            "nested_pages": content.get('nested_pages', {})
        }
        return json.dumps(structured_data, indent=4)
    except Exception as e:
        print(f"Error synthesizing JSON document: {e}")
        return None

def synthesize_text(content):
    """
    Converts the extracted content into a plain text format.
    
    :param content: The extracted content
    :return: Plain text version of the content
    """
    text_data = []
    # Combine headings and paragraphs into a single text structure
    for tag, texts in content.items():
        if tag.startswith('h') or tag == 'p':
            for text in texts:
                text_data.append(f"{tag.upper()}: {text}")
        elif tag == 'nested_pages':
            text_data.append("\nNested Pages:\n")
            for link, nested_content in content['nested_pages'].items():
                text_data.append(f"Link: {link}\n")
                text_data.append(synthesize_text(nested_content))
                
    return "\n".join(text_data)
