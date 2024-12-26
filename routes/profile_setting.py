import os
from flask import Blueprint, jsonify, request

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile_setting', methods=["POST"])
def profile_setting():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Validate required fields
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "Both email and password are required"}), 400

        # Save email and password as environment variables
        os.environ["UEMAIL"] = email
        os.environ["PASSWORDS"] = password

        return jsonify({"message": "Profile settings saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profile_bp.route('/profile_setting', methods=["GET"])
def get_profile_setting():
    try:
        # Retrieve the saved environment variables
        email = os.environ.get("UEMAIL", "")
        password = os.environ.get("PASSWORDS", "")

        if not email or not password:
            return jsonify({"error": "No profile settings found"}), 404

        return jsonify({"email": email, "password": password}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
