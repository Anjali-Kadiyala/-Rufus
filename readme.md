### Rufus - A Tool for Intelligent Web Data Extraction for LLMs

## Summary

### Objective
The aim is to develop Rufus, a dynamic web scraping AI agent that can extract targeted information based on user-defined instructions, and give output that integrates with RAG systems.

### Approach
1. LLM Integration: Integrated ChatGPT API to intelligently determine relevant elements for scraping based on user prompts. The input to ChatGPT API are tags, classes, ids, and first 50 characters of text to determine relevance with respect to the prompt.
2. Scraper Implementation: Built a scraper (scraper.py) using Selenium and BeautifulSoup. Implemented a depth based scraper and element extraction based on the relevant tags, classes, and IDs.
3. Client Implementation: Cleated RufusClient (client.py) for easy integration with external systems/ RAG systems. Client sends and receives responses from Flask API (app.py).
4. API Design: Developed a RESTful API using Flask (app.py).
5. Output: JSON file is saved in the cwd, as well as you can see the JSON output in the terminal.

## Challenges Faced 

### Nested/ Recursive Scraping
Error in code lead to infinite recursive loop, which consumed time to debug. Also managine nested pages while respecting domain boundaries was difficult.
Solution: Implemented a recursive function with depth control, and domain restrictions using urljoin to ensure only relevant links were followed. 

### Handling Dynamic Pages
Repeated faced super high page load times, and super slow processing due to javascript-loaded content. It required Selenium for browser automation. 
Solution: Setup appropriate timeouts in the setup_driver function. 

### Error with RufusClient
app.py is accessible/working when tested with Postman/ curl, but unable to make the call using test_rufus.py script. I will try to ressolve this as soon as possible.

