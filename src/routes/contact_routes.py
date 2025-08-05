from flask import Blueprint, jsonify, request
from src.models.contact_model import ContactOption
from src.models.contact_model import OfficeLocation,GlobalOffices,RegionalContact,ContactDirectory,SupportAgent,SupportTeam,ContactBox,ContactMessage

contact_bp = Blueprint('contact', __name__)

@contact_bp.route("/all-contacts", methods=["GET"])
def get_contacts():
    try:
        contacts = ContactOption.objects()
        contact_list = []

        for contact in contacts:
            contact_dict = contact.to_mongo().to_dict()
            contact_dict["_id"] = str(contact_dict["_id"])  
            contact_list.append(contact_dict)

        return jsonify(contact_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@contact_bp.route("/add-contact", methods=["POST"])
def add_contact():
    try:
        data = request.get_json()
        print(data)
        contact = ContactOption(
            title=data["title"],
            image=data["image"],
            Salesalt=data["Salesalt"],
            salesemail=data["salesemail"],
            Updatealt=data["Updatealt"],
            UpdateEmail=data["UpdateEmail"]
        )
        contact.save()

        return jsonify({"message": "Contact added successfully"}), 200

    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500




@contact_bp.route('/offices', methods=['POST'])
def create_offices():
    try:
        data = request.get_json()
        company_name = data.get('company_name')
        office_list = data.get('offices', [])

        if not company_name or not office_list:
            return jsonify({'error': 'Missing required fields'}), 400

        office_objects = []
        for office in office_list:
            office_obj = OfficeLocation(
                region=office.get('region'),
                address=office.get('address'),
                phone=office.get('phone'),
                city=office.get('city'),
                country=office.get('country'),
                image_url=office.get('image_url')
            )
            office_objects.append(office_obj)

        new_entry = GlobalOffices(company_name=company_name, offices=office_objects)
        new_entry.save()

        return jsonify({'message': 'Global offices added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contact_bp.route('/get-all-offices', methods=['GET'])
def get_all_offices():
    try:
        offices_data = GlobalOffices.objects().first()
        if not offices_data:
            return jsonify({'message': 'No office data found'}), 404

        result = {
            "company_name": offices_data.company_name,
            "offices": []
        }

        for office in offices_data.offices:
            result["offices"].append({
                "region": office.region,
                "address": office.address,
                "phone": office.phone,
                "city": office.city,
                "country": office.country,
                "image_url": office.image_url
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
 
    
@contact_bp.route('/create-regional-contact', methods=['POST'])
def create_regional_contacts():
    try:
        data = request.get_json()
        title = data.get('title', 'Regional Contacts')
        contacts_data = data.get('contacts', [])

        if not contacts_data:
            return jsonify({'error': 'Contacts data is required'}), 400

        contact_list = []
        for item in contacts_data:
            contact = RegionalContact(
                region=item.get('region'),
                phones=item.get('phones', []),
                email=item.get('email'),
                image_url=item.get('image_url')
            )
            contact_list.append(contact)

        directory = ContactDirectory(title=title, contacts=contact_list)
        directory.save()

        return jsonify({'message': 'Regional contacts created successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@contact_bp.route('/get-regional-contacts', methods=['GET'])
def get_regional_contacts():
    try:
        directory = ContactDirectory.objects().first()
        if not directory:
            return jsonify({'message': 'No regional contacts found'}), 404

        result = {
            'title': directory.title,
            'contacts': []
        }

        for contact in directory.contacts:
            result['contacts'].append({
                'region': contact.region,
                'phones': contact.phones,
                'email': contact.email,
                'image_url': contact.image_url
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@contact_bp.route('/support-team', methods=['POST'])
def create_regional_contact():
    try:
        data = request.get_json()
        team_title = data.get('team_title', 'Our Support Team')
        agents_data = data.get('agents', [])

        if not agents_data:
            return jsonify({'error': 'Agents list is required'}), 400

        agents = []
        for agent in agents_data:
            agent_doc = SupportAgent(
                name=agent['name'],
                role=agent['role'],
                email=agent['email'],
                image_url=agent['image_url'],
                social_links=agent.get('social_links', [])
            )
            agents.append(agent_doc)

        support_team = SupportTeam(team_title=team_title, agents=agents)
        support_team.save()

        return jsonify({'message': 'Regional contact created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    
@contact_bp.route('/get-support-team', methods=['GET'])
def get_all_support_teams():
    try:
        support_teams = SupportTeam.objects()

        response_data = []
        for team in support_teams:
            agents = []
            for agent in team.agents:
                agents.append({
                    'name': agent.name,
                    'role': agent.role,
                    'email': agent.email,
                    'image_url': agent.image_url,
                    'social_links': agent.social_links
                })

            response_data.append({
                'team_title': team.team_title,
                'agents': agents
            })

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    




@contact_bp.route('/get-in-touch', methods=['POST'])
def create_get_in_touch():
    try:
        data = request.get_json()

        contact_message = ContactMessage(
            full_name=data['full_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            message=data['message']
        )

        
        try:
            contact_box = ContactBox.objects.get(form_title="Get in Touch")
            contact_box.messages.append(contact_message)
        except:
            contact_box = ContactBox(messages=[contact_message])

        contact_box.save()

        return jsonify({'message': 'Contact message saved successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    
@contact_bp.route('/get-all-in-touch', methods=['GET'])
def get_all_get_in_touch():
    try:
        contact_boxes = ContactBox.objects()

        result = []
        for box in contact_boxes:
            box_data = {
                'form_title': box.form_title,
                'messages': []
            }
            for msg in box.messages:
                box_data['messages'].append({
                    'full_name': msg.full_name,
                    'email': msg.email,
                    'phone_number': msg.phone_number,
                    'message': msg.message
                })
            result.append(box_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



