from flask import Flask, jsonify, render_template
from flask_jwt_extended import jwt_required
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from models import User, db, init_app  # Make sure init_app is imported
from routes.campaign_api import campaign_bp
from routes.gen_route import cxo_finder_bp, dashboard_bp, view_leads_bp
from routes.insights import insights_bp
from routes.log_in import init_app_jwt, login_bp
from routes.research import research_bp
from routes.submit_cxo import cxo_submit_bp
from routes.profile_setting import profile_bp

# from flask_restful import Resource, Api


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:test1234@localhost:5432/flask_database"
app.config["SECRET_KEY"] = "SECRET!"

# Initialize the database
init_app(app) 
init_app_jwt(app)

# Initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = "login.login"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
# @jwt_required()
def health_check():
    return jsonify({"status": "healthy", "message": "Connection established"}), 200


# Register blueprints for Login
app.register_blueprint(login_bp)

# Register blueprints for CXO finder
app.register_blueprint(cxo_finder_bp)

# Register blueprints for Dashboard
app.register_blueprint(dashboard_bp)

# Register blueprints for Leads
app.register_blueprint(view_leads_bp)

# Register blueprints for company details
app.register_blueprint(research_bp)

# Register blueprints for Insights
app.register_blueprint(insights_bp)

# Register blueprints for Insights
app.register_blueprint(cxo_submit_bp)

# Register blueprints for campaign
app.register_blueprint(campaign_bp)

# Register blueprints for campaign
app.register_blueprint(profile_bp)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)