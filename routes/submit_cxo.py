from flask import Blueprint, render_template, request
from flask_login import login_required

from models import CompanyInfo, db
from settings import ENV
from utils.commons import getting_cxo_result

env = ENV()

cxo_submit_bp = Blueprint('cxo_submit', __name__)

@cxo_submit_bp.route("/submit_cxo", methods=["POST"])
def submit_cxo():
    # Get JSON payload from the request
    data = request.get_json()
    print(data)

    # Extracting fields from the JSON payload
    query = data.get('query')
    email = data.get('email')
    titles = data.get('titles', '')
    seniority = data.get('seniority', '')
    function = data.get('function', '')

    # Prepare the content payload for fetching CXO results
    content_payload = {
        "query": query,
        "positions": titles,
        "email": email
    }

    print("Content Payload:", content_payload)

    try:
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
            print('Ingesting:', new_company_info)
            db.session.add(new_company_info)

        db.session.commit()  # Commit all changes to the database
        
        return {"status": "success", "message": "Data ingested successfully"}, 200

    except Exception as e:
        # Handle any errors and roll back the session if necessary
        db.session.rollback()
        print("Error occurred:", str(e))
        return {"status": "error", "message": "Failed to ingest data", "error": str(e)}, 500
