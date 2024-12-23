from flask import Blueprint, jsonify, redirect, request, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_login import login_required, login_user, logout_user
from werkzeug.security import \
    check_password_hash  # For secure password comparison

from models import User  # Import the User model

# Initialize JWTManager
jwt = JWTManager()

def init_app_jwt(app):
    jwt.init_app(app)

# Login Blueprint
login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    print('The username is', username)
    print('The password is', password)
    
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:  # In production, use hashed passwords
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'success': True,
            'message': 'Login successfully',
            'data': {'token': access_token}
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid username or password'
        }), 400

# Logout Blueprint
logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
