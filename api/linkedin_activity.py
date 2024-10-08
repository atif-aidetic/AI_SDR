import requests
from bs4 import BeautifulSoup
from settings import ENV

env = ENV()

linkedin_api_key = env.linkedin_proxy_curl_api_key
linkedin_api_endpoint = env.linkedin_api_endpoint


def get_linkedin_post(linkedin_profile_url):
    result = []
    api_key = linkedin_api_key
    headers = {"Authorization": "Bearer " + api_key}

    api_endpoint = linkedin_api_endpoint

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=headers
    )

    if response.status_code == 200:
        scraped_data = response.json()

        if "activities" in scraped_data:
            shared_posts = scraped_data["activities"]  # Extract the activities

            # Process and store the shared posts
            for post in shared_posts:
                dict_res = {
                    "title": post.get("title"),
                    "link": post.get("link"),
                    "activity_status": post.get("activity_status"),
                }
                result.append(dict_res)  # Append each post's data to result

        else:
            print("No shared posts found in the scraped data.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

    return result


def extract_linkedin_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            full_text = soup.get_text(separator=" ", strip=True)
            return full_text
        else:
            return "Could not fetch the post content."
    except Exception as e:
        return f"Error occurred: {str(e)}"


# Example usage
# linkedin_profile_url = 'http://www.linkedin.com/in/amy-wright-1018941'
# linkedin_posts = get_linkedin_post(linkedin_profile_url)
# print(linkedin_posts)
# print(linkedin_posts)
