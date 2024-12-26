import requests
from flask import Blueprint, jsonify, request
from flask_login import login_required

from open_ai import generate_cold_message_openai
from sentiment_chart import create_sentiment_plot
from settings import ENV

env = ENV()

insight_data_api_url = env.insight_data_api

insights_bp = Blueprint('insights', __name__)


@insights_bp.route('/insight', methods=['POST'])
def insights():
    # Extract data from the JSON body
    data = request.get_json()

    company_domain = data.get('company_domain', "")
    company_name = data.get('company_name', "")
    linkedin_url = data.get('linkedin_url', "")
    name = data.get('name', "")
    title = data.get('title', "")
    email = data.get('email', "")

    if not company_name or not name:
        return jsonify({"error": "company_name and name are required"}), 400

    email_history = []

    # Generate LinkedIn message
    user_prompt_1 = f"write a linkedin message to {name} the {title} of {company_name}"
    try:
        linked_message = generate_cold_message_openai(user_prompt_1)
    except Exception as e:
        linked_message = None
        print(f"Error generating LinkedIn message: {e}")

    # Example sentiment values (replace with real analysis if available)
    try:
        sentiment_data = {
            "positive": 50,
            "negative": 30,
            "neutral": 20,
        }
    except Exception as e:
        sentiment_data = {"positive": 0, "negative": 0, "neutral": 0}
        print(f"Error generating sentiment data: {e}")

    # Prepare the response as JSON
    response = {
        "company_name": company_name,
        "company_domain": company_domain,
        "linkedin_url": linkedin_url,
        "name": name,
        "title": title,
        "email": email,
        "email_history": email_history,
        "linked_message": linked_message,
        "sentiment_data": sentiment_data,  # Includes positive, negative, and neutral
    }

    return jsonify(response), 200
