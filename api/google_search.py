import requests
from bs4 import BeautifulSoup
from settings import ENV

env = ENV()

google_api_key = env.google_api_key
google_cse_id = env.google_cse_id

# Function to perform Google Custom Search
def google_search_result(query):
    api_key = google_api_key
    cse_id = google_cse_id
    result = []
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"
    response = requests.get(url)
    search_results = response.json()
    results = []
    for item in search_results["items"]:
        result = {
            "title": item["title"],
            "description": item.get(
                "snippet", item["pagemap"]["metatags"][0].get("twitter:description", "")
            ),
            "url": item["link"],
        }
        results.append(result)

    return results


# Function to extract full text from a URL
def extract_google_text(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all the text from the page
            full_text = soup.get_text(separator=" ", strip=True)
            return full_text
        else:
            return "Could not fetch the article content."
    except Exception as e:
        return f"Error occurred: {str(e)}"
