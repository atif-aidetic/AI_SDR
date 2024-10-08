from flask import Blueprint, render_template
from flask_login import login_required
import requests
from open_ai import generate_cold_message_openai
from sentiment_chart import create_sentiment_plot
from settings import ENV

env = ENV()

insight_data_api_url = env.insight_data_api

insights_bp = Blueprint('insights', __name__)


@insights_bp.route("/insights/<string:company_domain>")
@login_required
def insights(company_domain):
    print("The company domain:", company_domain)

    try:
        response = requests.get(insight_data_api_url)
        response.raise_for_status()
        leads_data = response.json()
        leads = leads_data["data"]
        print(leads)

        # Filter leads to find those for the specific company
        company_leads = [
            lead for lead in leads if lead["company_domain"] == company_domain
        ]

        if not company_leads:
            # If no leads are found, handle this case
            return render_template(
                "insights.html",
                company_domain=company_domain,
                email_history=[],
                linked_message="",
                company_name="No data found",
                chart=None,
            )

        name = company_leads[0].get("name", "No data found")
        title = company_leads[0].get("title", "No data found")
        company_name = company_leads[0].get("company_name", "No data found")

        total_mails = [lead["mail"] for lead in company_leads if "mail" in lead]


        if total_mails:
            user_prompt_1 = f"write a linkedin message to {name} the {title} of {company_name}"

            linked_message = generate_cold_message_openai(user_prompt_1)
            print(linked_message)

        else:
            linked_message = ""

        # Example sentiment values
        positive = 50
        negative = 30
        neutral = 20

        chart = create_sentiment_plot(positive, negative, neutral)

        return render_template(
            "insights.html",
            company_domain=company_domain,
            email_history=company_leads,
            linked_message=linked_message,
            company_name=company_name,
            chart=chart,
        )

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        # Handle the case where the API request fails
        return render_template(
            "insights.html",
            company_domain=company_domain,
            email_history=[],
            linked_message="",
            company_name="No data found",
            chart=None,
        )
