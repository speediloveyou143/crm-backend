from flask import Flask
from flask_cors import CORS
from src.config.database import init_db
from src.routes.user_routes import user_bp

from src.routes.contact_routes import contact_bp

from src.routes.features_route import features_bp
from src.routes.pricing_routes import pricing_bp

from dotenv import load_dotenv
import os
from src.routes.privacy_policy_routes import privacy_policy_bp


load_dotenv()
print(os.getenv('JWT_KEY'))  
print(os.getenv('FRONTEND_ORIGIN')) 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_KEY')  


# Initialize MongoDB connection
init_db()


frontend_origin = os.getenv('FRONTEND_ORIGIN')
if not frontend_origin:
    raise ValueError("FRONTEND_ORIGIN is not set in .env file")

CORS(app, 
     resources={r"/api/*": {"origins": [frontend_origin], "supports_credentials": True}},
     methods=['GET', 'POST', 'OPTIONS'],  
     allow_headers=['Content-Type', 'Authorization']  
)


app.register_blueprint(user_bp, url_prefix='/api/users')

app.register_blueprint(privacy_policy_bp,url_prefix='/api/privacy')
app.register_blueprint(contact_bp, url_prefix='/api/contact')
app.register_blueprint(features_bp,url_prefix='/api/features')

@app.route("/",methods=["GET"])
def home():
    return "home"
app.register_blueprint(pricing_bp, url_prefix='/api/pricing')


if __name__ == '__main__':
    app.run(debug=True,host="localhost")