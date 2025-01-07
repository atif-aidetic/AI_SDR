from flask import Blueprint, jsonify, request

from api.google_search import google_search_result
from api.linkedin_activity import get_linkedin_post
from api.news_search import get_news
from open_ai import generate_cold_email_openai
from settings import ENV

env = ENV()

cold_data_api_url = env.cold_data_api

research_bp = Blueprint('company_name', __name__)

@research_bp.route('/research', methods=['POST'])
def view_company_details():
    # Extract data from the JSON body
    print("Entering into research")
    data = request.get_json()

    company_name = data.get('company_name', "")
    company_domain = data.get('company_domain', "")
    linkedin_url = data.get('linkedin_url', "")
    title = data.get('title', "")
    email = data.get('email', "")
    name = data.get('name', "")
    # Extract 'name' from the JSON body

    try:
        news_articles = get_news(company_name) if company_name else []
    except Exception as e:
        news_articles = []
        print(f"Error fetching news articles: {e}")

    try:
        google_search_list = google_search_result(company_name) if company_name else []
    except Exception as e:
        google_search_list = []
        print(f"Error fetching Google search results: {e}")

    try:
        linkedin_search_list = []  # Placeholder for LinkedIn search results
        # Uncomment and implement if LinkedIn search functionality is added
        # linkedin_search_list = get_linkedin_post(linkedin_url) if linkedin_url else []
    except Exception as e:
        linkedin_search_list = []
        print(f"Error fetching LinkedIn search results: {e}")

    if company_name and name:
        email_id = email
        user_prompt_1 = "write a mail to {} the {} of {}".format(
            name,
            title,
            company_name,
        )
        subject, body = None, None
        while subject is None or body is None:
            subject, body = generate_cold_email_openai(user_prompt_1)
    else:
        email_id = None
        subject = ""
        body = ""

    # Prepare the result as a JSON response
    result = {
        "company_name": company_name,
        "name": name,
        "company_domain": company_domain,
        "linkedin_url": linkedin_url,
        "title": title,
        "email": email,
        "news_articles": news_articles,
        "google_search_list": google_search_list,
        "linkedin_search_list": linkedin_search_list,
        "email_id": email_id,
        "email_subject": subject,
        "email_body": body,
    }

    return jsonify(result), 200