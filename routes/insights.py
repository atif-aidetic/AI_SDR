import requests
from flask import Blueprint, render_template, request
from flask_login import login_required

from open_ai import generate_cold_message_openai
from sentiment_chart import create_sentiment_plot
from settings import ENV

env = ENV()

insight_data_api_url = env.insight_data_api

insights_bp = Blueprint('insights', __name__)


@insights_bp.route('/insight/<company_name>', methods=['GET'])
@login_required
def insights(company_name):
    print("The company domain:------------------>", company_name)

    date_added = request.args.get('date_added')
    company_domain = request.args.get('company_domain')
    company_name = request.args.get('company_name')
    linkedin_url = request.args.get('linkedin_url')
    name = request.args.get('name')
    title = request.args.get('title')
    email = request.args.get('email')

    if not company_name:
        # If no leads are found, handle this case
        return render_template(
            "insights.html",
            company_name=company_name,
            email_history=[],
            linked_message="",
            chart=None,
        )

    name = name
    title = title
    company_name = company_name
    email_history = []


    user_prompt_1 = f"write a linkedin message to {name} the {title} of {company_name}"

    linked_message = generate_cold_message_openai(user_prompt_1)
    print(linked_message)


    # Example sentiment values
    positive = 50
    negative = 30
    neutral = 20

    chart = create_sentiment_plot(positive, negative, neutral)

    return render_template(
        "insights.html",
        company_name=company_name,
        email_history=email_history,
        linked_message=linked_message,
        chart=chart,
    )

    # except requests.exceptions.RequestException as e:
    #     print(f"API request error: {e}")
    #     # Handle the case where the API request fails
    #     return render_template(
    #         "insights.html",
    #         company_domain=company_domain,
    #         email_history=[],
    #         linked_message="",
    #         company_name="No data found",
    #         chart=None,
    #     )
