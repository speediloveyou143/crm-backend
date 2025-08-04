from flask import Blueprint, jsonify, request
from src.models.pricing_model import PlanItem,PersonalPricing,BusinessPricing,PricingPlan,FeatureSet,FAQItem,FAQSection

pricing_bp = Blueprint('pricing', __name__)

@pricing_bp.route('/add-personal-plan', methods=["POST"])
def add_personal_plan():
    data = request.get_json()
    if data:
        # Create a new PlanItem from the data
        plan_item = PlanItem(
            plan_name=data["plan_name"],
            price=data["price"],
            billing=data["billing"],
            description=data["description"],
            features=data["features"]
        )

        # Fetch the first (or create new) PersonalPricing document
        personal_pricing = PersonalPricing.objects.first()
        if not personal_pricing:
            personal_pricing = PersonalPricing(plans=[plan_item])
        else:
            personal_pricing.plans.append(plan_item)

        personal_pricing.save()
        return jsonify({"message": "Plan added successfully"}), 200
    else:
        return jsonify({"message": "Error while adding plan"}), 400


@pricing_bp.route('/get-personal-plans', methods=["GET"])
def get_personal_plans():
    personal_pricing = PersonalPricing.objects.first()
    if personal_pricing and personal_pricing.plans:
        plans = []
        for plan in personal_pricing.plans:
            plans.append({
                "plan_name": plan.plan_name,
                "price": plan.price,
                "billing": plan.billing,
                "description": plan.description,
                "features": plan.features
            })
        return jsonify({"plans": plans}), 200
    else:
        return jsonify({"message": "No personal plans found"}), 404




#Business plan routes
@pricing_bp.route('/add-business-plan', methods=["POST"])
def add_business_plan():
    data = request.get_json()
    if data:
        # Create a new PlanItem for business
        plan_item = PlanItem(
            plan_name=data["plan_name"],
            price=data["price"],
            billing=data["billing"],
            description=data["description"],
            features=data["features"]
        )

        # Fetch the first (or create new) BusinessPricing document
        business_pricing = BusinessPricing.objects.first()
        if not business_pricing:
            business_pricing = BusinessPricing(plans=[plan_item])
        else:
            business_pricing.plans.append(plan_item)

        business_pricing.save()
        return jsonify({"message": "Business plan added successfully"}), 200    
    else:
        return jsonify({"message": "Error while adding business plan"}), 400
    


@pricing_bp.route('/get-business-plans', methods=["GET"])
def get_business_plans():
    business_pricing = BusinessPricing.objects.first()
    if business_pricing and business_pricing.plans:
        plans = []
        for plan in business_pricing.plans:
            plans.append({
                "plan_name": plan.plan_name,
                "price": plan.price,
                "billing": plan.billing,
                "description": plan.description,
                "features": plan.features
            })
        return jsonify({"plans": plans}), 200
    else:
        return jsonify({"message": "No business plans found"}), 404



#compare plans Routes

@pricing_bp.route('/add-compare-plan', methods=['POST'])
def add_compare_plan():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    feature_data = data.get("features")
    features = FeatureSet(**feature_data)

    plan = PricingPlan(
        plan_name=data["plan_name"],
        features=features
    )
    plan.save()
    return jsonify({"message": "Plan added successfully"}), 201

# Route to get all plans
@pricing_bp.route('/get-compare-plans', methods=['GET'])
def get_compare_plans():
    plans = PricingPlan.objects()
    return jsonify([{
        "plan_name": plan.plan_name,
        "features": {
            "users": plan.features.users,
            "whatsapp_conversations": plan.features.whatsapp_conversations,
            "lead_management": plan.features.lead_management,
            "analytics_dashboard": plan.features.analytics_dashboard,
            "multi_agent_support": plan.features.multi_agent_support
        }
    } for plan in plans])


#FAQ section
@pricing_bp.route('/add-faq-section', methods=['POST'])
def add_faq_section():
    data = request.get_json()
    if not data or 'category' not in data or 'faqs' not in data:
        return jsonify({"error": "Invalid data"}), 400

    faq_items = [FAQItem(**item) for item in data['faqs']]
    section = FAQSection(category=data['category'], faqs=faq_items)
    section.save()

    return jsonify({"message": "FAQ section added successfully"}), 201


@pricing_bp.route('/get-faqs', methods=['GET'])
def get_faqs():
    sections = FAQSection.objects()
    return jsonify([
        {
            "category": section.category,
            "faqs": [
                {
                    "question": faq.question,
                    "answer": faq.answer
                } for faq in section.faqs
            ]
        } for section in sections
    ])
