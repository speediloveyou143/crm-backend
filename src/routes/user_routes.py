from flask import Blueprint, request, jsonify, make_response, current_app
import jwt
import datetime
import bcrypt
from functools import wraps
from ..models.user_model import User

user_bp = Blueprint('user', __name__)





@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
       
        required_fields = ['name', 'email', 'phone_number', 'password']
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
            role='user'
        )
        user.save()

        
        token = jwt.encode({
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        
        response = make_response(jsonify({
            'message': 'User created successfully',
            'user': {'name': user.name, 'email': user.email, 'role': user.role}
        }))
        response.set_cookie('token', token, httponly=True, max_age=24*60*60, samesite='Lax', secure=True)
        return response, 201

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





@user_bp.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Invalid input'}), 400

        user = User.objects(email=data['email']).first()
        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401

       
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
        response.set_cookie('token', token, httponly=True, max_age=24*60*60, samesite='Lax', secure=True)
        return response, 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500
