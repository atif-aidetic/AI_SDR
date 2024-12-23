import requests
from flask import Blueprint, render_template, request
from flask_login import login_required

from api.google_search import google_search_result
from api.linkedin_activity import get_linkedin_post
from api.news_search import get_news
from open_ai import generate_cold_email_openai
from settings import ENV

env = ENV()

cold_data_api_url = env.cold_data_api

research_bp = Blueprint('company_name', __name__)


@research_bp.route('/research/<company_name>', methods=['GET'])
@login_required
def view_company_details(company_name):
    # Extract data from the query parameters
    date_added = request.args.get('date_added')
    company_domain = request.args.get('company_domain')
    company_name = request.args.get('company_name')
    linkedin_url = request.args.get('linkedin_url')
    name = request.args.get('name')
    title = request.args.get('title')
    email = request.args.get('email')

    try:
        if company_name:
            news_articles = get_news(company_name)
            # news_articles = []
        else:
            news_articles = []
    except:
        news_articles = []

    try:
        if company_name:
            google_search_list = google_search_result(company_name)
            # google_search_list = []
        else:
            google_search_list = []
    except:
        google_search_list = []

    try:
        if company_name:
            # linkedin_search_list = get_linkedin_post(linkedin_url)
            # linkedin_search_list
            linkedin_search_list = []
        else:
            linkedin_search_list = []
    except:
        linkedin_search_list = []

    if company_name:
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
        cold_mail_gen = []
        subject = ""
        body = ""

    # Pass the data to the template
    return render_template(
        "company_details.html",
        company_domain=company_domain,
        news_articles=news_articles,
        google_search_list=google_search_list,
        linkedin_search_list=linkedin_search_list,
        email_id=email_id,
        subject=subject,
        body=body,
    )