from flask import Flask
from flask_cors import CORS
from src.config.database import init_db
from src.routes.user_routes import user_bp
from src.routes.features_route import features_bp
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
print(os.getenv('JWT_KEY'))  # Debug print to verify JWT_KEY is loaded
print(os.getenv('FRONTEND_ORIGIN'))  # Debug print to verify FRONTEND_ORIGIN is loaded

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_KEY')  # Load secret key from .env

@app.route("/",methods=["GET"])
def home():
    return "home"

# Initialize MongoDB connection
init_db()

# Configure CORS to allow requests from frontend origin with proper preflight handling
frontend_origin = os.getenv('FRONTEND_ORIGIN')
if not frontend_origin:
    raise ValueError("FRONTEND_ORIGIN is not set in .env file")

CORS(app, 
     resources={r"/api/*": {"origins": [frontend_origin], "supports_credentials": True}},
     methods=['GET', 'POST', 'OPTIONS'],  # Explicitly allow OPTIONS for preflight
     allow_headers=['Content-Type', 'Authorization']  # Allow necessary headers
)

# Register Blueprints with url_prefix
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(features_bp,url_prefix='/api/features')


if __name__ == '__main__':
    app.run(debug=True,host="localhost")