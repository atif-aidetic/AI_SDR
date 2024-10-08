from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import requests
from settings import ENV

env = ENV()

news_api = env.news_api


def get_news(start_up_name):
    result = []
    newsapi = NewsApiClient(api_key=news_api)

    # Get news articles mentioning the specific startup
    top_headlines = newsapi.get_everything(
        q=start_up_name, language="en", sort_by="relevancy"
    )

    # Print and store the results
    for article in top_headlines["articles"]:
        dict_res = {
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
        }
        result.append(dict_res)

    return result


def extract_news_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract all the text from the page
        full_text = soup.get_text(separator=" ", strip=True)

        return full_text
    else:
        return "Could not fetch the article content."
    