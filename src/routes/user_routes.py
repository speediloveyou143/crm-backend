from flask import Blueprint, request, jsonify, make_response
from flask import current_app  # Import current_app
import jwt
import datetime
import bcrypt
from ..models.user_model import User

user_bp = Blueprint('user', __name__)

# Signup API
@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        # Validate required fields
        required_fields = ['name', 'email', 'phone_number', 'password',"company_Name","business_Type"]  # Removed 'role' to match frontend
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # Check if user already exists
        if User.objects(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create new user with hashed password
        user = User(
            name=data['name'],
            email=data['email'],
            phone_number=data.get('phone_number', ''),  # Use phone_number to match frontend 'mobile'
            password=hashed_password,
            company_Name=data["company_Name"],
            business_Type=data["business_Type"],
            role='user'  # Default role since frontend doesn't send it
        )
        user.save()

        # Generate JWT
        token = jwt.encode({
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")  # Use current_app instead of request.app

        # Set cookie
        response = make_response(jsonify({
            'message': 'User created successfully',
            'user': {'name': user.name, 'email': user.email, 'role': user.role,'phone_number':user.phone_number,'business_Type':user.business_Type,'company_Name':user.company_Name}
        }))
        response.set_cookie('token', token, httponly=False, max_age=24*60*60, samesite='Lax', secure=False)
        response.set_cookie('id', str(user.id), httponly=False, max_age=24*60*60, samesite='Lax', secure=False)
        return response, 200

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

        # Generate JWT
        token = jwt.encode({
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")  # Use current_app instead of request.app

        # Set cookie
        response = make_response(jsonify({
            'message': 'Login successful',
            'user': {'name': user.name, 'email': user.email, 'role': user.role}
        }))
        response.set_cookie('token', token, httponly=True, max_age=24*60*60, samesite='Lax', secure=True)
        return response, 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500