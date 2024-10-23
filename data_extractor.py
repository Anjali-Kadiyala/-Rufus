# rufus/data_extractor.py

from bs4 import BeautifulSoup
import json

def extract_content(soup, tag, css_class=None):
    """
    Extracts specific content based on the HTML tag and optional CSS class provided.
    
    :param soup: BeautifulSoup object containing the page source
    :param tag: HTML tag (e.g., 'div', 'p', 'h1')
    :param css_class: Optional CSS class to further filter the elements
    :return: List of extracted content blocks as strings
    """
    if css_class:
        elements = soup.find_all(tag, class_=css_class)
    else:
        elements = soup.find_all(tag)
        
    content_blocks = [element.get_text(strip=True) for element in elements if element.get_text(strip=True)]
    return content_blocks

def clean_data(content_blocks):
    """
    Cleans the extracted data by removing duplicates and filtering out certain patterns.
    
    :param content_blocks: List of extracted content strings
    :return: Cleaned list of content
    """
    cleaned_blocks = []
    seen_blocks = set()
    for block in content_blocks:
        if block not in seen_blocks and not block.lower().startswith(('powered by', 'original text', 'select language')):
            seen_blocks.add(block)
            cleaned_blocks.append(block)
    return cleaned_blocks


def extract_news(soup):
    """
    Extracts news headlines and descriptions from the page based on the website structure.
    
    :param soup: BeautifulSoup object containing the page source
    :return: List of news articles as dictionaries
    """
    # Update these tags and classes based on the website’s actual structure
    news_headlines = extract_content(soup, 'h2', 'headline')  # Replace 'headline' with the actual class name
    news_summaries = extract_content(soup, 'p', 'summary')    # Replace 'summary' with the actual class name
    
    # If the summaries are not present, you may extract just headlines
    if not news_summaries:
        news_articles = [{'headline': headline} for headline in news_headlines]
    else:
        news_articles = [{'headline': headline, 'summary': summary} for headline, summary in zip(news_headlines, news_summaries)]
    
    return news_articles

def extract_events(soup):
    """
    Extracts events information including titles and dates.
    
    :param soup: BeautifulSoup object containing the page source
    :return: List of events as dictionaries
    """
    event_titles = extract_content(soup, 'h3', 'event-title')  # Customize the tag and class based on the website structure
    event_dates = extract_content(soup, 'p', 'event-date')  # Customize accordingly
    
    events = [{'title': title, 'date': date} for title, date in zip(event_titles, event_dates)]
    return events

def extract_jobs(soup):
    """
    Extracts job postings including titles and descriptions.
    
    :param soup: BeautifulSoup object containing the page source
    :return: List of job postings as dictionaries
    """
    job_titles = extract_content(soup, 'h4', 'job-title')  # Customize the tag and class based on the website structure
    job_descriptions = extract_content(soup, 'p', 'job-description')  # Customize accordingly
    
    jobs = [{'title': title, 'description': description} for title, description in zip(job_titles, job_descriptions)]
    return jobs

def structure_data(data, data_type):
    """
    Structures the extracted data based on the type (e.g., news, events, jobs).
    
    :param data: Data to be structured
    :param data_type: Type of data ('news', 'events', 'jobs')
    :return: Structured data in JSON format
    """
    cleaned_content = clean_data(data)
    return json.dumps({data_type: cleaned_content}, indent=4)

def extract_and_structure(soup, content_type):
    """
    Combines extraction and structuring for a specific content type.
    
    :param soup: BeautifulSoup object containing the page source
    :param content_type: Type of content to extract ('news', 'events', 'jobs')
    :return: Structured JSON data
    """
    if content_type == 'news':
        return structure_data(extract_news(soup), 'news')
    elif content_type == 'events':
        return structure_data(extract_events(soup), 'events')
    elif content_type == 'jobs':
        return structure_data(extract_jobs(soup), 'jobs')
    else:
        return json.dumps({"error": "Unsupported content type"}, indent=4)
