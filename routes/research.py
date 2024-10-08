from flask import Blueprint, render_template
from flask_login import login_required
import requests
from api.linkedin_activity import get_linkedin_post
from api.google_search import google_search_result
from api.news_search import get_news
from open_ai import generate_cold_email_openai
from settings import ENV

env = ENV()

cold_data_api_url = env.cold_data_api

company_domain_bp = Blueprint('company_domain', __name__)

@company_domain_bp.route("/company/<company_domain>", methods=["GET"])
@login_required
def view_company_details(company_domain):
    # Retrieve all leads from the API
    response = requests.get(cold_data_api_url)
    response.raise_for_status()
    leads_data = response.json()
    leads = leads_data["data"]

    # Filter leads to find those for the specific company
    company_leads = [lead for lead in leads if lead["company_domain"] == company_domain]


    try:
        if company_leads:
            company_name = company_leads[0]["company_name"]
            news_articles = get_news(company_name)
            # news_articles = []
        else:
            news_articles = []
    except:
        news_articles = []

    try:
        if company_leads:
            company_name = company_leads[0]["company_name"]
            google_search_list = google_search_result(company_name)
            # google_search_list = []
        else:
            google_search_list = []
    except:
        google_search_list = []

    try:
        if company_leads:
            linkedin_url = company_leads[0]["linkedin_url"]
            linkedin_search_list = get_linkedin_post(linkedin_url)
            linkedin_search_list
            # linkedin_search_list = []
        else:
            linkedin_search_list = []
    except:
        linkedin_search_list = []

    if company_leads:
        email_id = company_leads[0]["email"]
        user_prompt_1 = "write a mail to {} the {} of {}".format(
            company_leads[0]["name"],
            company_leads[0]["title"],
            company_leads[0]["company_name"],
        )
        subject, body = None, None
        while subject is None or body is None:
            subject, body = generate_cold_email_openai(user_prompt_1)
    else:
        cold_mail_gen = []
        subject = ""
        body = ""

    return render_template(
        "company_details.html",
        company_leads=company_leads,
        company_domain=company_domain,
        news_articles=news_articles,
        google_search_list=google_search_list,
        linkedin_search_list=linkedin_search_list,
        email_id=email_id,
        subject=subject,
        body=body,
    )
    