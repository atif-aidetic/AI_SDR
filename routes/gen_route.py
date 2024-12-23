import requests
from flask import Blueprint, render_template
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


view_leads_bp = Blueprint('view_leads', __name__)

@view_leads_bp.route('/leads', methods=["GET"])
@login_required
def view_leads():
    try:
        # Query all data from the company_info table
        leads = CompanyInfo.query.all()
        
        # Convert SQLAlchemy objects to dictionaries for easier use in the template
        leads_list = [
            {
                "id": lead.id,
                "company_name": lead.company_name,
                "company_domain": lead.company_domain,
                "name": lead.name,
                "linkedin_url": lead.linkedin_url,
                "title": lead.title,
                "email": lead.email,
                "date_added": lead.date_added
            }
            for lead in leads
        ]
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        leads_list = []

    return render_template("leads.html", leads=leads_list)
