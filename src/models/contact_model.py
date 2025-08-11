from mongoengine import Document, StringField, EmailField,ListField,EmbeddedDocument,EmbeddedDocumentField

class ContactOption(Document):
    title = StringField(required=True)
    image = StringField(required=True)
    
    Salesalt = StringField(required=True)
    salesemail = EmailField(required=True)

    Updatealt = StringField(required=True)
    UpdateEmail = EmailField(required=True)

    meta = {'collection': 'contacts'}

class OfficeLocation(EmbeddedDocument):
    region = StringField(required=True)  
    address = StringField(required=True)
    phone = StringField(required=True)
    city = StringField()
    country = StringField()
    image_url = StringField()  


class GlobalOffices(Document):
    company_name = StringField(required=True)
    offices = ListField(EmbeddedDocumentField(OfficeLocation))
    meta = {'collection': 'globaloffice'}
    
    
    
    
    
class RegionalContact(EmbeddedDocument):
    region = StringField(required=True)        
    phones = ListField(StringField())          
    email = StringField(required=True)         
    image_url = StringField()                  


class ContactDirectory(Document):
    title = StringField(required=True, default="Regional Contacts")
    contacts = ListField(EmbeddedDocumentField(RegionalContact))
    meta = {'collection': 'regional_contacts'}
    
    

class SupportAgent(EmbeddedDocument):
    name = StringField(required=True)
    role = StringField(required=True)  
    email = EmailField(required=True)
    image_url = StringField(required=True)
    social_links = ListField(StringField())  



class SupportTeam(Document):
    team_title = StringField(required=True, default="Our Support Team")
    agents = ListField(EmbeddedDocumentField(SupportAgent))
    meta = {'collection': 'support_team'}


 
 
class ContactMessage(EmbeddedDocument):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField(required=True)
    message = StringField(required=True)


class ContactBox(Document):
    form_title = StringField(required=True, default="Get in Touch")
    messages = ListField(EmbeddedDocumentField(ContactMessage))
    meta = {'collection': 'contact_box'}
    
    