from mongoengine import Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField,BooleanField


class PlanItem(EmbeddedDocument):
    plan_name = StringField(required=True)
    price = StringField()
    billing = StringField()
    description = StringField()
    features = ListField(StringField())
    button_text = StringField(default="Get Plan")
    button_class = StringField(default="bg-indigo-500 hover:bg-indigo-600")



class PersonalPricing(Document):
    plans = ListField(EmbeddedDocumentField(PlanItem))
    meta = {'collection': 'personal_pricing'}



class BusinessPricing(Document):
    plans = ListField(EmbeddedDocumentField(PlanItem))
    meta = {'collection': 'business_pricing'}



class FeatureSet(EmbeddedDocument):
    users = StringField(required=True)  
    whatsapp_conversations = StringField(required=True)  
    lead_management = StringField(required=True)  
    analytics_dashboard = StringField(required=True)  
    multi_agent_support = BooleanField(default=False)

class PricingPlan(Document):
    plan_name = StringField(required=True, unique=True) 
    features = EmbeddedDocumentField(FeatureSet)
    meta = {'collection': 'compare_plans'}




class FAQItem(EmbeddedDocument):
    question = StringField(required=True)
    answer = StringField(required=True)

class FAQSection(Document):
    category = StringField(required=True)  
    faqs = ListField(EmbeddedDocumentField(FAQItem))
    meta = {'collection': 'faq_section'}