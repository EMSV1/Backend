from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required  # Importing jwt_required
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


# Only HR can create or edit joining details
@joining_bp.route("/joining", methods=["POST"])
@jwt_required()  # Ensure that JWT is verified
@role_required(roles=["HR"])
def create_joining():
    data = request.json
    new_joining = Joining(
        employee_id=data["employee_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
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


# Get joining details for a specific employee (Accessible to HR only)
@joining_bp.route("/joining/<int:id>", methods=["GET"])
@jwt_required()  # Ensure that JWT is verified
@role_required(roles=["HR"])
def get_joining(id):
    joining = Joining.query.get(id)
    if not joining:
        return jsonify({"message": "Joining not found"}), 404
    return jsonify(
        {
            "employee_id": joining.employee_id,
            "first_name": joining.first_name,
            "last_name": joining.last_name,
            "business_unit": joining.business_unit,
            "business_title": joining.business_title,
            "resource_type": joining.resource_type,
            "contact_number": joining.contact_number,
            "reporting_manager": joining.reporting_manager,
            "employment_status": joining.employment_status,
            "created_date": joining.created_date,
            "last_modified_date": joining.last_modified_date,
        }
    )


# Get all joining details (Accessible to HR only)
@joining_bp.route("/joining", methods=["GET"])
@jwt_required()  # Ensure that JWT is verified
@role_required(roles=["HR"])
def get_all_joining():
    joinings = Joining.query.all()  # Fetch all joining records
    if not joinings:
        return jsonify({"message": "No joinings found"}), 404

    # Convert each joining record to a dictionary and return as a list
    result = []
    for joining in joinings:
        result.append(
            {
                "employee_id": joining.employee_id,
                "first_name": joining.first_name,
                "last_name": joining.last_name,
                "business_unit": joining.business_unit,
                "business_title": joining.business_title,
                "resource_type": joining.resource_type,
                "contact_number": joining.contact_number,
                "reporting_manager": joining.reporting_manager,
                "employment_status": joining.employment_status,
                "created_date": joining.created_date,
                "last_modified_date": joining.last_modified_date,
            }
        )
    return jsonify(result)


# Update joining details for a specific employee (Accessible to HR only)
@joining_bp.route("/joining/<int:id>", methods=["PUT"])
@jwt_required()  # Ensure that JWT is verified
@role_required(roles=["HR"])
def update_joining(id):
    data = request.json
    joining = Joining.query.get(id)
    if not joining:
        return jsonify({"message": "Joining not found"}), 404
    joining.first_name = data.get("first_name", joining.first_name)
    joining.last_name = data.get("last_name", joining.last_name)
    joining.business_unit = data.get("business_unit", joining.business_unit)
    joining.business_title = data.get("business_title", joining.business_title)
    joining.resource_type = data.get("resource_type", joining.resource_type)
    joining.contact_number = data.get("contact_number", joining.contact_number)
    joining.reporting_manager = data.get("reporting_manager", joining.reporting_manager)
    joining.employment_status = data.get("employment_status", joining.employment_status)
    db.session.commit()
    return jsonify({"message": "Joining updated successfully"})
