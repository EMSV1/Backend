from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from requirements.__init__ import db
from models import Joining
from requirements.auth import role_required
from flask_cors import CORS

joining_bp = Blueprint("joining_bp", __name__)

CORS(
    joining_bp,
    origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "https://cogs-354de766c1e7.herokuapp.com",
    ],
    supports_credentials=True,
)

# Create a new joining record (Accessible to HR and Super-Admin)
@joining_bp.route("/joining", methods=["POST"])
@jwt_required()
@role_required(roles=["HR", "Super-Admin"])
def create_joining():
    data = request.json
    new_joining = Joining(
        employee_id=data["employee_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        emp_email_id=data["emp_email_id"],
        employee_address=data["employee_address"],
        business_unit=data["business_unit"],
        business_title=data["business_title"],
        resource_type=data["resource_type"],
        contact_number=data["contact_number"],
        reporting_manager=data["reporting_manager"],
        employment_status=data["employment_status"],
    )
    db.session.add(new_joining)
    db.session.commit()
    return jsonify({"message": "Joining created successfully"}), 201

# Get a specific joining record by ID (Accessible to HR and Super-Admin)
@joining_bp.route("/joining/<int:id>", methods=["GET"])
@jwt_required()
@role_required(roles=["HR", "Super-Admin"])
def get_joining(id):
    joining = Joining.query.get(id)
    if not joining:
        return jsonify({"message": "Joining not found"}), 404
    return jsonify(joining.to_dict())

# Get all joining records (Accessible to HR and Super-Admin)
@joining_bp.route("/joining", methods=["GET"])
@jwt_required()
@role_required(roles=["HR", "Super-Admin"])
def get_all_joining():
    joinings = Joining.query.all()
    return jsonify([joi.to_dict() for joi in joinings])

# Update a specific joining record by ID (Accessible to HR and Super-Admin)
@joining_bp.route("/joining/<int:id>", methods=["PUT"])
@jwt_required()
@role_required(roles=["HR", "Super-Admin"])
def update_joining(id):
    data = request.json
    joining = Joining.query.get(id)
    if not joining:
        return jsonify({"message": "Joining not found"}), 404

    for key, value in data.items():
        if hasattr(joining, key):
            setattr(joining, key, value)
    db.session.commit()
    return jsonify({"message": "Joining updated successfully"})

# Delete a specific joining record by ID (Accessible to HR and Super-Admin)
@joining_bp.route("/joining/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required(roles=["HR", "Super-Admin"])
def delete_joining(id):
    joining = Joining.query.get(id)
    if not joining:
        return jsonify({"message": "Joining not found"}), 404

    db.session.delete(joining)
    db.session.commit()
    return jsonify({"message": "Joining deleted successfully"})
