from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

class URLRequest(BaseModel):
    url: str

def scrape_data(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all('a', href=True)

    filtered_links = [
        link.get('href')
        for link in links
        if link.get('href') and link.get('href').startswith(
            ("https://www.canadianmortgagetrends.com/", "https://www.bizjournals.com/", "https://www.zoocasa.com/blog")
        )
    ]

    # Convert the list of links to JSON
    return json.dumps(filtered_links, indent=4)

@app.post("/scrape/")
def scrape_links(request: URLRequest):
    links_json = scrape_data(request.url)
    return {"links": json.loads(links_json)}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Link Scraper API. Use the /scrape/ endpoint to scrape links."}
