from mongoengine import Document, StringField, EmbeddedDocumentField, EmbeddedDocument, ListField

class Badge(EmbeddedDocument):
    badge_label = StringField()
    badge_sub_label = StringField()
    badge_color = StringField()

class Features(Document):
    name = StringField(required=True)
    icon_name = StringField(required=True) 
    icon_class_name = StringField(required=True)
    content = StringField(required=True)
    bg_color = StringField(required=True)
    hover_bg_color = StringField(required=True)
    badge = EmbeddedDocumentField(Badge)

