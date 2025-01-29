from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_cors import CORS

# Create Blueprint for login functionality
login_bp = Blueprint("login_bp", __name__)

# Enable CORS for the login blueprint with proper configuration
CORS(
    login_bp,
    resources={
        r"/login": {
            "origins": [
                "http://localhost:3000",
                "http://localhost:8080",
                "http://127.0.0.1:8080",
                "http://127.0.0.1:3000",
                "https://cogs-354de766c1e7.herokuapp.com",
                "https://www.v97-cems.com"
            ],
            "methods": ["POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True,
        }
    },
)


@login_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        return response

    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    if user and check_password_hash(user.password, data["password"]):
        role_name = user.role.role_name if user.role else "User"

        access_token = create_access_token(
            identity=str(user.id), additional_claims={"role": role_name}
        )

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "user": {"id": user.id, "email": user.email, "role": role_name},
                }
            ),
            200,
        )

    return jsonify({"message": "Invalid credentials"}), 401
