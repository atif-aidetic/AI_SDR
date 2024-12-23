from flask import request, jsonify, Blueprint
from datetime import datetime
from models import Campaign, db
from flask_jwt_extended import jwt_required


# Login Blueprint
campaign_bp = Blueprint('campaign', __name__)

# API to retrieve all campaigns
@campaign_bp.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    try:
        campaigns = Campaign.query.all()
        result = [
            {
                "campaign_name": campaign.campaign_name,
                "domain": campaign.domain,
                "created_by": campaign.created_by,
                "date_created": campaign.date_created.strftime('%Y-%m-%d'),
                "is_active": campaign.is_active
            }
            for campaign in campaigns
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to add a new campaign
@campaign_bp.route('/api/campaigns', methods=['POST'])
def add_campaign():
    data = request.json
    try:
        # Validate required fields
        required_fields = ["campaign_name", "domain", "created_by", "date_created", "is_active"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' is required"}), 400

        # Validate date format
        try:
            date_created = datetime.strptime(data["date_created"], "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format, should be YYYY-MM-DD"}), 400

        # Check if campaign already exists
        if Campaign.query.filter_by(campaign_name=data["campaign_name"]).first():
            return jsonify({"error": "Campaign with this name already exists"}), 400

        # Add new campaign to the database
        new_campaign = Campaign(
            campaign_name=data["campaign_name"],
            domain=data["domain"],
            created_by=data["created_by"],
            date_created=date_created,
            is_active=data["is_active"]
        )
        db.session.add(new_campaign)
        db.session.commit()

        return jsonify({"message": "Campaign added successfully", "campaign": data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
