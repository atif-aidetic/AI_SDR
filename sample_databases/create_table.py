from datetime import datetime

import pytz
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test1234@localhost:5432/flask_database'

db = SQLAlchemy(app)

# Function to get current time in IST
def current_time_ist():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

class CompanyInfo(db.Model):
    __tablename__ = 'company_info'  # Uncomment to specify table name explicitly
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255), nullable=True, default=None)
    company_domain = db.Column(db.String(255), nullable=True, default=None)
    name = db.Column(db.String(255), nullable=True, default=None)
    linkedin_url = db.Column(db.String(255), nullable=True, default=None)
    title = db.Column(db.String(255), nullable=True, default=None)
    email = db.Column(db.String(255), nullable=True, default=None)
    date_added = db.Column(db.DateTime, nullable=False, default=current_time_ist)
    
class User(db.Model, UserMixin):
    __tablename__ = 'user_name'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
# Define Campaign model
class Campaign(db.Model):
    __tablename__ = 'campaign'
    campaign_name = db.Column(db.String, primary_key=True)
    domain = db.Column(db.String, nullable=False)
    created_by = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)


with app.app_context():
    db.create_all()