from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField, ListField, EmbeddedDocumentField
)

class Section(EmbeddedDocument):
    heading = StringField()
    description = StringField()
    points = ListField(StringField())

class PrivacyPolicy(Document):
    sections = ListField(EmbeddedDocumentField(Section))
    meta = {'collection': 'privacy_policies'}
