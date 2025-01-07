# backend/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    """
    Factory function to create the Flask app and initialize extensions, blueprints, etc.
    """
    # Initialize the Flask app
    app = Flask(__name__)

    # Load configurations from the config.py file
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Initialize CORS (Allow specific origins for development)
    CORS(app, origins=["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000"], supports_credentials=True)

    # Register blueprints (routes)
    from routes import  requirement, approval, interview, joining, assets, licenses, login, users
    from requirements.auth import user_routes  # Import user_routes blueprint for role assignment

    # Register the blueprints with URL prefixes
    # app.register_blueprint(employee.employee_bp, url_prefix='/employee')
    app.register_blueprint(requirement.requirements_bp, url_prefix='/')
    app.register_blueprint(approval.approval_bp, url_prefix='/approval')
    app.register_blueprint(interview.interview_bp, url_prefix='/interview')
    app.register_blueprint(joining.joining_bp, url_prefix='/')
    app.register_blueprint(assets.assets_bp, url_prefix='/')
    app.register_blueprint(licenses.licenses_bp, url_prefix='/')

    # Register user and login blueprints
    app.register_blueprint(users.user_bp, url_prefix='/users')
    app.register_blueprint(user_routes, url_prefix='/users')  # Register role assignment blueprint
    app.register_blueprint(login.login_bp, url_prefix='/')

    return app
