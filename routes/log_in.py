from flask import Blueprint, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user, login_required
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from models import User  # Import the User model

login_bp = Blueprint('login', __name__)

class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Check user and password
            login_user(user)
            return redirect(url_for("cxo_finder.new_1"))  # Redirect to the index route
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)



logout_bp = Blueprint('login', __name__)

@logout_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))