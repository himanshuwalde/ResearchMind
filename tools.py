from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    results = tavily.search(query = query, max_results= 5)

    out = []

    for r in results["results"]:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n")


    return "\n---\n".join(out)

@tool
def web_scrape(url : str) -> str:
    """Scrape the content of a webpage. Returns the text content of the page."""
    try:
        response = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape the webpage. Error: {str(e)}"

