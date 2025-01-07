from flask import Blueprint, request, jsonify
from models import Requirement
from requirements.__init__ import db
from requirements.auth import role_required
from flask_jwt_extended import jwt_required  # Import this to require JWT validation
from flask_cors import CORS

requirements_bp = Blueprint("requirements_bp", __name__)

CORS(
    requirements_bp,
    origins=["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000", "https://cogs-354de766c1e7.herokuapp.com"],
    supports_credentials=True,
)


# Only Admin roles can create or edit requirements
@requirements_bp.route("/requirements", methods=["POST"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin"])
def create_requirement():
    data = request.json
    new_requirement = Requirement(
        business_unit=data["business_unit"],
        resource_requirement=data["resource_requirement"],
        job_description=data["job_description"],
        resource_type=data["resource_type"],
        business_title=data["business_title"],
        vector_title=data["vector_title"],
        comments=data.get("comments", ""),
        department=data["department"],
    )
    db.session.add(new_requirement)
    db.session.commit()
    return jsonify({"message": "Requirement created successfully"}), 201


# Get all requirements (Accessible to Admin only)
@requirements_bp.route("/requirements", methods=["GET"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin"])
def get_requirements():
    requirements = Requirement.query.all()
    result = [
        req.to_dict() for req in requirements
    ]  # Using to_dict() for serialization
    return jsonify(result)


# Get a specific requirement (Accessible to Admin only)
@requirements_bp.route("/requirements/<int:id>", methods=["GET"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin"])
def get_requirement(id):
    requirement = Requirement.query.get(id)
    if not requirement:
        return jsonify({"message": "Requirement not found"}), 404
    return jsonify(requirement.to_dict())  # Using to_dict() for serialization


# Update a requirement (Accessible to Admin only)
@requirements_bp.route("/requirements/<int:id>", methods=["PUT"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin"])
def update_requirement(id):
    data = request.json
    requirement = Requirement.query.get(id)
    if not requirement:
        return jsonify({"message": "Requirement not found"}), 404
    requirement.business_unit = data.get("business_unit", requirement.business_unit)
    requirement.resource_requirement = data.get(
        "resource_requirement", requirement.resource_requirement
    )
    requirement.job_description = data.get(
        "job_description", requirement.job_description
    )
    requirement.resource_type = data.get("resource_type", requirement.resource_type)
    requirement.business_title = data.get("business_title", requirement.business_title)
    requirement.vector_title = data.get("vector_title", requirement.vector_title)
    requirement.comments = data.get("comments", requirement.comments)
    requirement.department = data.get("department", requirement.department)
    db.session.commit()
    return jsonify({"message": "Requirement updated successfully"})


# Delete a requirement (Accessible to Admin only)
@requirements_bp.route("/requirements/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin"])
def delete_requirement(id):
    requirement = Requirement.query.get(id)
    if not requirement:
        return jsonify({"message": "Requirement not found"}), 404
    db.session.delete(requirement)
    db.session.commit()
    return jsonify({"message": "Requirement deleted successfully"})
