from flask import Blueprint, request, jsonify
from src.models.privacy_policy import PrivacyPolicy, Section

privacy_policy_bp = Blueprint('privacy_policy', __name__)


@privacy_policy_bp.route('/privacy-policy', methods=['POST'])
def create_privacy_policy():
    try:
        data = request.get_json()
        sections_data = data.get("sections", [])
        sect = []

        for sec in sections_data:
            section = Section(
                heading=sec.get("heading"),
                description=sec.get("description"),
                points=sec.get("points", [])
            )
            sect.append(section)

        policy = PrivacyPolicy(sections=sect)
        policy.save()

        return jsonify({"message": "Privacy policy created successfully"}), 201

    except Exception as e:
     
        print("Error:", e)
        return jsonify({"message": "error"}), 500


@privacy_policy_bp.route('/get-privacy-policy', methods=['GET'])
def get_privacy_policy():
    try:
        policies = PrivacyPolicy.objects()
        if not policies:
            return jsonify({"message": "No privacy policy found"}), 404

        
        result = []
        for policy in policies:
            sections = []
            for sec in policy.sections:
                sections.append({
                     "heading": sec.heading,
                    "description": sec.description,
                    "points": sec.points
                })
            result.append({"id": str(policy.id), "sections": sections})

        return jsonify(result), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error fetching privacy policies"}), 500


