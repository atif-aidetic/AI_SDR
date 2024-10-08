from flask import Flask, render_template
from flask_login import LoginManager
from routes.log_in import login_bp
from routes.gen_route import cxo_finder_bp, dashboard_bp, view_leads_bp
from routes.insights import insights_bp
from routes.research import company_domain_bp
from models import db, User 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "SECRET!"

# Initialize the database
db.init_app(app)

# Initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = "login.login"

@app.route("/")
def index():
    return render_template("index.html")

# Register blueprints for Login
app.register_blueprint(login_bp)

# Register blueprints for CXO finder
app.register_blueprint(cxo_finder_bp)

# Register blueprints for Dashboard
app.register_blueprint(dashboard_bp)

# Register blueprints for Leads
app.register_blueprint(view_leads_bp)

# Register blueprints for company details
app.register_blueprint(company_domain_bp)

# Register blueprints for Insights
app.register_blueprint(insights_bp)


# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
