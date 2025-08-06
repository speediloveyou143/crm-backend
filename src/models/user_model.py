from mongoengine import Document, StringField, EmailField, DateTimeField ,DictField, ListField ,EmbeddedDocument ,FloatField ,EmbeddedDocumentField
from datetime import datetime,timedelta

class Location(EmbeddedDocument): 
    city=StringField()
    state=StringField()
    longitude=StringField()
    latitude=StringField()

class Current_Pay(EmbeddedDocument):
    current_plan=StringField()
    started_at=DateTimeField()
    valid_upto = DateTimeField()
    amount=StringField(required=True,default='free')
    payment_id=StringField()

    
class UserField(EmbeddedDocument):
    field_type = StringField(required=True)
    field_name = StringField(required=True)
    options = ListField(StringField()) 
    required=StringField(required=True)

class User(Document):
    name = StringField(required=True,max_length=100)
    email = EmailField(required=True, unique=True)
    phone_number = StringField(required=True, max_length=15,unique=True)
    password = StringField(required=True)
    location = EmbeddedDocumentField(Location)
    role = StringField(choices=['user', 'admin','super_admin'], default='user')
    business_Type = StringField(required=True)
    company_Name = StringField(required=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()
    current_pay = EmbeddedDocumentField(Current_Pay)
    all_Pays = ListField(EmbeddedDocumentField(Current_Pay))
    user_Fields = ListField(EmbeddedDocumentField(UserField)) 
    user_leads = ListField(DictField())
    meta = {'collection': 'users','db_alias':'default'}


