from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime

class User(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    phone_number = StringField(required=True, max_length=15)
    password = StringField(required=True)
    role = StringField(required=True, choices=['user', 'admin'], default='user')
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'users'}