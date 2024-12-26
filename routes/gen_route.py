import requests
from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from models import CompanyInfo, db
from settings import ENV

env = ENV()

cold_data_api_url = env.cold_data_api

cxo_finder_bp = Blueprint('cxo_finder', __name__)

@cxo_finder_bp.route("/new_1", methods=["GET", "POST"])
@login_required
def new_1():
    return render_template("new_1.html")

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


## API for leads
view_leads_bp = Blueprint('view_leads', __name__)

@view_leads_bp.route('/leads', methods=["GET"])
def view_leads():
    try:
        campaign_name = request.args.get('campaign_name', None)

        if campaign_name:
            company_info = CompanyInfo.query.filter_by(campaign_name=campaign_name).all()
        else:
            return jsonify({"error": "Missing campaign_name parameter"}), 400

        # Prepare the result
        result = [
            {
                "company_name": company.campaign_name,
                "company_domain": company.company_domain,
                "name": company.name,
                "linkedin_url": company.linkedin_url,
                "title": company.title,
                "email": company.email,
                "date_added": company.date_added
            }
            for company in company_info
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@view_leads_bp.route('/leads', methods=["POST"])
def add_lead():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Validate required fields
        required_fields = ["campaign_name", "company_name", "company_domain", "name", "linkedin_url", "title", "email", "date_added"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Create a new CompanyInfo instance
        new_lead = CompanyInfo(
            campaign_name=data["campaign_name"],
            company_name=data["company_name"],
            company_domain=data["company_domain"],
            name=data["name"],
            linkedin_url=data["linkedin_url"],
            title=data["title"],
            email=data["email"],
            date_added=data["date_added"]  # Ensure this is in the correct format
        )

        # Add and commit the new lead to the database
        db.session.add(new_lead)
        db.session.commit()

        return jsonify({"message": "Lead added successfully", "lead_id": new_lead.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@view_leads_bp.route('/leads/<int:lead_id>', methods=["PUT"])
def update_lead(lead_id):
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Query the lead to be updated
        lead = CompanyInfo.query.get(lead_id)
        if not lead:
            return jsonify({"error": f"Lead with ID {lead_id} not found"}), 404

        # Update fields if provided in the request
        if "campaign_name" in data:
            lead.campaign_name = data["campaign_name"]
        if "company_domain" in data:
            lead.company_domain = data["company_domain"]
        if "name" in data:
            lead.name = data["name"]
        if "linkedin_url" in data:
            lead.linkedin_url = data["linkedin_url"]
        if "title" in data:
            lead.title = data["title"]
        if "email" in data:
            lead.email = data["email"]
        if "date_added" in data:
            lead.date_added = data["date_added"]

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": f"Lead with ID {lead_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@view_leads_bp.route('/leads/<int:lead_id>', methods=["DELETE"])
def delete_lead(lead_id):
    try:
        # Query the lead to be deleted
        lead = CompanyInfo.query.get(lead_id)
        if not lead:
            return jsonify({"error": f"Lead with ID {lead_id} not found"}), 404

        # Delete the lead
        db.session.delete(lead)
        db.session.commit()

        return jsonify({"message": f"Lead with ID {lead_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
