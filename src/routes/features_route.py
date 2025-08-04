from flask import Blueprint, request, jsonify
from ..models.features import Features, Badge, Feature

features_bp = Blueprint('features_bp', __name__)

# POST: /set-features
@features_bp.route('/set-features', methods=["POST"])
def setFeatures():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"message": "Expected a list of features"}), 400

        features_list = []
        for feature_data in data:
            badge_data = feature_data.get("badge", {})
            feature = Feature(
                name=feature_data["name"],
                icon_name=feature_data["icon_name"],
                icon_class_name=feature_data["icon_class_name"],
                content=feature_data["content"],
                bg_color=feature_data["bg_color"],
                hover_bg_color=feature_data["hover_bg_color"],
                badge=Badge(
                    badge_label=badge_data.get("badge_label", ""),
                    badge_sub_label=badge_data.get("badge_sub_label", ""),
                    badge_color=badge_data.get("badge_color", "")
                )
            )
            features_list.append(feature)

        features_doc = Features(data=features_list)
        features_doc.save()

        return jsonify({"message": "Data saved successfully"}), 200

    except Exception as e:
        print("Error in setFeatures:", str(e))
        return jsonify({"message": "Failed to save data", "error": str(e)}), 500


# GET: /all-features
@features_bp.route('/all-features', methods=["GET"])
def allFeatures():
    try:
        all_features_docs = Features.objects()
        response = []

        for doc in all_features_docs:
            for feature in doc.data:
                response.append({
                    "name": feature.name,
                    "icon_name": feature.icon_name,
                    "icon_class_name": feature.icon_class_name,
                    "content": feature.content,
                    "bg_color": feature.bg_color,
                    "hover_bg_color": feature.hover_bg_color,
                    "badge": {
                        "badge_label": feature.badge.badge_label if feature.badge else "",
                        "badge_sub_label": feature.badge.badge_sub_label if feature.badge else "",
                        "badge_color": feature.badge.badge_color if feature.badge else ""
                    }
                })

        return jsonify(response), 200
    except Exception as e:
        print("Error in allFeatures:", str(e))
        return jsonify({"message": "Failed to fetch data", "error": str(e)}), 500
