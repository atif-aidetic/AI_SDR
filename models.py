from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

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
        self.company_domain = company_domain
        self.name = name
        self.linkedin_url = linkedin_url
        self.title = title
        self.email = email

    def __repr__(self):
        return f'<Lead {self.name} at {self.company_name}>'
