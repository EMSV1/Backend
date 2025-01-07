from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, User, Role
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('users', __name__)

# Create User Endpoint (Assign Admin role by default)
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()

    # Check if email is already registered
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'])

    # Create new user and assign the Admin role (role_id = 1 for Admin)
    new_user = User(
        email=data['email'],
        password=hashed_password,
        role_id=1  # Default role: Admin
    )

    # Add new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user": data['email']}), 201


# Assign Role to User (Admin only)
@user_bp.route('/<int:user_id>/assign_role', methods=['PUT'])
@jwt_required()
def assign_role(user_id):
    data = request.get_json()

    # Get the current user's ID from the JWT token
    current_user_id = get_jwt_identity()

    # Fetch the current user from the database using current_user_id
    current_user = User.query.get(current_user_id)

    # Ensure the current user is an Admin (by checking the role of the current user)
    if current_user is None or current_user.role is None or current_user.role.role_name != 'Admin':
        return jsonify({"message": "Access denied. Admins only."}), 403

    # Fetch the requested role from the database
    role = Role.query.filter_by(role_name=data['role_name']).first()
    if not role:
        return jsonify({"message": "Role not found"}), 404

    # Fetch the user to whom the role should be assigned
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Assign the new role to the user
    user.role_id = role.role_id
    db.session.commit()

    return jsonify({"message": f"Role {role.role_name} assigned to user {user.email}"}), 200