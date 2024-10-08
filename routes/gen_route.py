from flask import Blueprint, render_template
from flask_login import login_required
import requests
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
    api_url = cold_data_api_url
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        leads_data = response.json()
        leads = leads_data["data"]
        print(leads[0])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        leads = []
    return render_template("leads.html", leads=leads)
