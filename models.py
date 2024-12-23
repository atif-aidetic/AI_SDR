from datetime import datetime

import pytz
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    
# Function to get current time in IST
def current_time_ist():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

class User(db.Model, UserMixin):
    __tablename__ = 'user_name'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    company_domain = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    linkedin_url = db.Column(db.String(250), nullable=True)
    title = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, company_name, company_domain, name, linkedin_url, title, email):
        self.company_name = company_name
        self.company_domain = company_domain or 'N/A'  # Provide a default value
        self.name = name
        self.linkedin_url = linkedin_url
        self.title = title
        self.email = email


    def __repr__(self):
        return f'<Lead {self.name} at {self.company_name}>'
    
class CompanyInfo(db.Model):
    __tablename__ = 'company_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255), nullable=True, default=None)
    company_domain = db.Column(db.String(255), nullable=True, default=None)
    name = db.Column(db.String(255), nullable=True, default=None)
    linkedin_url = db.Column(db.String(255), nullable=True, default=None)
    title = db.Column(db.String(255), nullable=True, default=None)
    email = db.Column(db.String(255), nullable=True, default=None)
    date_added = db.Column(db.DateTime, nullable=False, default=current_time_ist)
    
    
class Campaign(db.Model):
    __tablename__ = 'campaign'
    campaign_name = db.Column(db.String, primary_key=True)
    domain = db.Column(db.String, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)