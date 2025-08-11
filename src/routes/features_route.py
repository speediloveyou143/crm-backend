from flask import Blueprint, request, jsonify
from ..models.features import Features, Badge

features_bp = Blueprint('features_bp', __name__)

# POST: /set-features
@features_bp.route('/set-features', methods=["POST"])
def setFeatures():
    try:
        data = request.get_json()
        if not isinstance(data, dict):  # Expect a single feature object
            return jsonify({"message": "Expected a feature object"}), 400

        badge_data = data.get("badge", {})
        feature = Features(
            name=data["name"],
            icon_name=data["icon_name"],
            icon_class_name=data["icon_class_name"],
            content=data["content"],
            bg_color=data["bg_color"],
            hover_bg_color=data["hover_bg_color"],
            badge=Badge(
                badge_label=badge_data.get("badge_label", ""),
                badge_sub_label=badge_data.get("badge_sub_label", ""),
                badge_color=badge_data.get("badge_color", "")
            ) if badge_data else None
        )
        result=feature.save()
        if result:
            return jsonify({"message": "Feature saved successfully"}), 200
        else:
            return jsonify({"message": "Feature not saved in DB"}), 404
    except Exception as e:
        print("Error in setFeatures:", str(e))
        return jsonify({"message": "Failed to save feature", "error": str(e)}), 500

# GET: /all-features
@features_bp.route('/all-features', methods=["GET"])
def allFeatures():
    try:
        all_features = Features.objects()
        response = [
            {
                "id": str(feature.id),
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
            } for feature in all_features
        ]
        if len(response)<=0:
            return jsonify({"message":"no data available in DB "}),203
        else:
            return jsonify({"message":"data fetched successfully ","data":response}), 200
    except Exception as e:
        print("Error in allFeatures:", str(e))
        return jsonify({"message": "Failed to fetch features", "error": str(e)}), 500

# GET: /get-feature/<id>
@features_bp.route('/get-feature/<id>', methods=["GET"])
def getFeature(id):
    try:
        feature = Features.objects(id=id).first()
        if not feature:
            return jsonify({"message": "Feature not found"}), 404

        response = {
            "id": str(feature.id),
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
        }

        if response:
            return jsonify({"message": "Feature retrieved successfully", "data": response}), 200
        else:
            return jsonify({"message": "Feature not found"}), 204
    except Exception as e:
        print("Error in getFeature:", str(e))
        return jsonify({"message": "Failed to fetch feature", "error": str(e)}), 500

# PUT: /update-feature/<id>
@features_bp.route('/update-feature/<id>', methods=["PUT"])
def updateFeature(id):
    try:
        feature = Features.objects(id=id).first()
        if not feature:
            return jsonify({"message": "Feature not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        # Update fields if provided
        feature.name = data.get("name", feature.name)
        feature.icon_name = data.get("icon_name", feature.icon_name)
        feature.icon_class_name = data.get("icon_class_name", feature.icon_class_name)
        feature.content = data.get("content", feature.content)
        feature.bg_color = data.get("bg_color", feature.bg_color)
        feature.hover_bg_color = data.get("hover_bg_color", feature.hover_bg_color)

        # Update badge if provided
        badge_data = data.get("badge", {})
        if badge_data:
            feature.badge = Badge(
                badge_label=badge_data.get("badge_label", feature.badge.badge_label if feature.badge else ""),
                badge_sub_label=badge_data.get("badge_sub_label", feature.badge.badge_sub_label if feature.badge else ""),
                badge_color=badge_data.get("badge_color", feature.badge.badge_color if feature.badge else "")
            )

        result=feature.save()
        if result:
            return jsonify({"message": "Feature updated successfully"}), 200
        else:
            return jsonify({"message": "Feature not updated"}), 204
    except Exception as e:
        print("Error in updateFeature:", str(e))
        return jsonify({"message": "Failed to update feature", "error": str(e)}), 500

# DELETE: /delete-feature/<id>
@features_bp.route('/delete-feature/<id>', methods=["DELETE"])
def deleteFeature(id):
    try:
        feature = Features.objects(id=id).first()
        if not feature:
            return jsonify({"message": "Feature not found"}), 404

        result=feature.delete()
        if result==None:
            return jsonify({"message": "Feature deleted successfully"}), 200
        else:
            return jsonify({"message": "Feature not deleted "}), 204
    except Exception as e:
        print("Error in deleteFeature:", str(e))
        return jsonify({"message": "Failed to delete feature", "error": str(e)}), 500