from flask import Blueprint, render_template, request
from flask_login import login_required

from models import CompanyInfo, db
from settings import ENV
from utils.commons import getting_cxo_result

env = ENV()

cxo_submit_bp = Blueprint('cxo_submit', __name__)

@cxo_submit_bp.route("/submit_cxo", methods=["GET", "POST"])
@login_required
def new_1():
    if request.method == "POST":
        query = request.form.get('query')
        email = request.form.get('email')
        titles = request.form.get('titles', '')
        seniority = request.form.get('seniority', '')
        function = request.form.get('function', '')

        content_payload = {
            "query": query,
            "positions": titles,
            "email": email
        }

        print("------------------>", content_payload)

        # Fetching CXO results
        response = getting_cxo_result(content_payload)

        # Save data to the company_info table
        for lead in response:
            new_company_info = CompanyInfo(
                company_name=lead.get('company_name', 'N/A'),
                company_domain=lead.get('company_domain', 'N/A'),
                name=lead.get('name', 'N/A'),
                linkedin_url=lead.get('linkedin_url', 'N/A'),
                title=lead.get('title', 'N/A'),
                email=lead.get('email', 'N/A')
            )
            print('Company Info data is ------------------_>', new_company_info)
            db.session.add(new_company_info)  # Add the new entry to the session

        db.session.commit()  # Commit all changes to the database
        return "CXO data submitted successfully", 200

    return render_template("submit_cxo.html")