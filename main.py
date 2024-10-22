# main.py

from agent import RufusAgent

def main():

    agent = RufusAgent()
    url = "https://sf.gov"
    tags = ['h1', 'h2', 'p', 'div']
    result = agent.run(url, tags=tags)
    
    print(result)

if __name__ == "__main__":
    main()
