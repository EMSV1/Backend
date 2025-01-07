from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from flask import Blueprint, request, jsonify, abort
from models import db, User, Role  # Ensure that User and Role models are imported
from werkzeug.security import generate_password_hash, check_password_hash


def role_required(roles):
    """
    This decorator ensures that the user has one of the required roles.
    The roles parameter should be a list of roles (e.g., ['Admin', 'HR']).
    """

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()  # This should return the user ID from the JWT
            user = User.query.get(user_id)  # Fetch user from the database

            # Ensure the user has a role and check if the role matches the allowed roles
            if user and user.role and user.role.role_name in roles:
                return fn(*args, **kwargs)

            return {"msg": "Permission denied"}, 403

        return wrapped

    return wrapper


# Blueprint for user-related routes
user_routes = Blueprint("user_routes", __name__)


# Assign Role to User (Admin only)
@user_routes.route("/users/<int:user_id>/assign_role", methods=["PUT"])
@jwt_required()  # Requires a valid JWT token
def assign_role(user_id):
    """
    Endpoint to assign a role to a user. Only Admin users can assign roles.
    """
    data = request.get_json()  # Get data from the request
    role = Role.query.filter_by(
        role_name=data["role_name"]
    ).first()  # Find the role by name

    if not role:
        return jsonify({"message": "Role not found"}), 404

    user = User.query.filter_by(id=user_id).first()  # Find the user by ID

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Assign the role to the user
    user.role_id = role.role_id
    db.session.commit()

    return (
        jsonify({"message": f"Role {role.role_name} assigned to user {user.email}"}),
        200,
    )


# Example role-based access control (for Admin users)
@user_routes.route("/admin-only", methods=["GET"])
@jwt_required()  # Requires a valid JWT token
def admin_only():
    """
    Example endpoint that only allows access to Admin users.
    """
    current_user = get_jwt_identity()  # Get the current user's identity from the JWT

    # Ensure the current user is an Admin
    user = User.query.get(current_user)
    if user and user.role.role_name != "Admin":
        abort(403, description="Access denied. Admins only.")

    return jsonify({"message": "This is an Admin-only endpoint."}), 200
