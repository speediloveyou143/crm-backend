from flask import Blueprint, request, jsonify, make_response, current_app
import jwt
import datetime
import bcrypt
from ..models.user_model import User
from..models.user_model import Location


user_bp = Blueprint('user', __name__)



#signup api
@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        # Validate required fields
        required_fields = ['name', 'email', 'phone_number', 'password',"company_Name","business_Type","location"]  # Removed 'role' to match frontend

        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

      
        if User.objects(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
          
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            name=data['name'],
            email=data['email'],
            phone_number=data.get('phone_number', ''),
            password=hashed_password,
            company_Name=data["company_Name"],
            business_Type=data["business_Type"],
            location=Location(
                city=location.get('city'),
                state=location.get('state'),
                longitude=location.get('longitude'),
                latitude=location.get('latitude')
            ),
            role='user'  # Default role since frontend doesn't send it
            )
        result=user.save()
        if result:
            return jsonify({"messge":"sign up successfull"}), 200
        else:
            return jsonify({"messge":"sign up failed"}), 404
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Signin API
@user_bp.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Invalid input'}), 400

        user = User.objects(email=data['email']).first()
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401

        # Verify password
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        token = jwt.encode({
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        
        response = make_response(jsonify({
            'message': 'Login successful',
            'user': {'name': user.name, 'email': user.email, 'role': user.role}
        }))
        response.set_cookie("token",token, httponly=False, max_age=24*60*60,samesite="LAX")
        response.set_cookie("id",str(user.id),httponly=False,max_age=24*60*60,samesite="LAX")
        return response, 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500
    



@user_bp.route('/all-users', methods=['GET'])
def get_all_users():
    try:
        users = User.objects()
        user_list = [{
            
            'name': user.name,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role
        } for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@user_bp.route('/get-user/<id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = User.objects.get(id=id)
        return jsonify({
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role
        }), 200
    except User.DoesNotExist:
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@user_bp.route('/update-user/<id>', methods=['PUT'])
def update_user_by_id(id):
    try:
        data = request.json
        user = User.objects.get(id=id)

        for field in ['name', 'email', 'phone_number', 'role']:
            if field in data:
                setattr(user, field, data[field])

        user.save()
        return jsonify({'message': 'User updated successfully'}), 200
    except User.DoesNotExist:
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@user_bp.route('/delete-user/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    except User.DoesNotExist:
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500



#Signin with google
@user_bp.route('/signIn-With-Google', methods=['POST'])
def SignInWithGoogle():

    try:
        data = request.get_json()
        if not data or 'email' not in data or 'name' not in data:
            return jsonify({'message': 'Invalid input'}), 400

        user = User.objects(email=data['email']).first()
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401

 
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'message': 'Invalid credentials'}), 401

        # Generate JWT

        token = jwt.encode({
            'email': user.email,
            # 'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

       
        response = make_response(jsonify({
            'message': 'Login successful',
            'user': {'name': user.name, 'email': user.email, 'role': user.role}
        }))
        response.set_cookie('token',token, httponly=False,samesite="LAX",secure=False)
        response.set_cookie("id",str(user.id),httponly=False,samesite="LAX",secure=False)
        return response, 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


    
@user_bp.route("/signout",methods=["POST"])
def sign_out():
    response=make_response("deleted")
    response.delete_cookie("token")
    response.delete_cookie("id")
    return response

