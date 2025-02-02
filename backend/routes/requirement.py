import pandas as pd
from io import BytesIO
from flask import Blueprint, request, jsonify, send_file
from models import Requirement, User, RequirementApproval, Role
from requirements.__init__ import db
from requirements.auth import role_required
from flask_jwt_extended import jwt_required  # Import this to require JWT validation
from flask_cors import CORS
from .email_utils import send_email


requirements_bp = Blueprint("requirements_bp", __name__)

CORS(
    requirements_bp,
    origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "https://cogs-354de766c1e7.herokuapp.com",
        "https://www.v97-cems.com/login"
    ],
    supports_credentials=True,
)

@requirements_bp.route("/requirements", methods=["POST"])
@jwt_required()
@role_required(roles=["Admin", "Super-Admin"])
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

    # Hardcoded email for testing
    super_admin_email = "cems1812@gmail.com"
    subject = "New Requirement Created"
    body = (
    f"New Requirement Created\n\n"
    f"Requirement Details:\n"
    f"-------------------\n"
    f"Business Unit: {new_requirement.business_unit}\n"
    f"Resource Requirement: {new_requirement.resource_requirement}\n"
    f"Job Description: {new_requirement.job_description}\n"
    f"Resource Type: {new_requirement.resource_type}\n"
    f"Business Title: {new_requirement.business_title}\n"
    f"Vector Title: {new_requirement.vector_title}\n"
    f"Comments: {new_requirement.comments}\n"
    f"Department: {new_requirement.department}\n"
    f"Created Date: {new_requirement.created_date}\n"
    f"Last Modified Date: {new_requirement.last_modified_date}\n\n"
    f"Please review the requirement at your earliest convenience."
)
    send_email(super_admin_email, subject, body)

    return jsonify({"message": "Requirement created successfully"}), 201


# @requirements_bp.route("/requirements", methods=["POST"])
# @jwt_required()
# @role_required(roles=["Admin", "Super-Admin"])
# def create_requirement():
#     data = request.json
#     new_requirement = Requirement(
#         business_unit=data["business_unit"],
#         resource_requirement=data["resource_requirement"],
#         job_description=data["job_description"],
#         resource_type=data["resource_type"],
#         business_title=data["business_title"],
#         vector_title=data["vector_title"],
#         comments=data.get("comments", ""),
#         department=data["department"],
#     )
#     db.session.add(new_requirement)
#     db.session.commit()

#     # Fetch Super Admin email dynamically by joining the Role table
#     super_admin_role = Role.query.filter_by(role_name="Super-Admin").first()
#     if super_admin_role:
#         super_admin_user = User.query.filter_by(role_id=super_admin_role.role_id).first()
#         if super_admin_user:
#             super_admin_email = super_admin_user.email
#             subject = "New Requirement Created"
#             body = f"A new requirement has been created:\n\n{new_requirement.to_dict()}"
#             send_email(super_admin_email, subject, body)

#     return jsonify({"message": "Requirement created successfully"}), 201

# Only Admin roles can create or edit requirements
# @requirements_bp.route("/requirements", methods=["POST"])
# @jwt_required()  # Ensure the request has a valid JWT token
# @role_required(roles=["Admin", "Super-Admin"])
# def create_requirement():
#     data = request.json
#     new_requirement = Requirement(
#         business_unit=data["business_unit"],
#         resource_requirement=data["resource_requirement"],
#         job_description=data["job_description"],
#         resource_type=data["resource_type"],
#         business_title=data["business_title"],
#         vector_title=data["vector_title"],
#         comments=data.get("comments", ""),
#         department=data["department"],
#     )
#     db.session.add(new_requirement)
#     db.session.commit()
#     return jsonify({"message": "Requirement created successfully"}), 201


# Get all requirements (Accessible to Admin only)
@requirements_bp.route("/requirements", methods=["GET"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin", "Super-Admin"])
def get_requirements():
    requirements = Requirement.query.all()
    result = [req.to_dict() for req in requirements]
    return jsonify({"count": len(requirements), "requirements": result})


# Get a specific requirement (Accessible to Admin only)
@requirements_bp.route("/requirements/<int:id>", methods=["GET"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin", "Super-Admin"])
def get_requirement(id):
    requirement = Requirement.query.get(id)
    if not requirement:
        return jsonify({"message": "Requirement not found"}), 404
    return jsonify(requirement.to_dict())  # Using to_dict() for serialization


# Update a requirement (Accessible to Admin only)
@requirements_bp.route("/requirements/<int:id>", methods=["PUT"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin", "Super-Admin"])
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
@role_required(roles=["Admin", "Super-Admin"])
def delete_requirement(id):
    requirement = Requirement.query.get(id)
    if not requirement:
        return jsonify({"message": "Requirement not found"}), 404
    db.session.delete(requirement)
    db.session.commit()
    return jsonify({"message": "Requirement deleted successfully"})

# Export all requirements to Excel (Download All Requirements)
@requirements_bp.route("/requirements/export", methods=["GET"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin", "Super-Admin"])  # Make sure only authorized users can access this
def export_requirements_to_excel():
    # Query all requirements from the database
    requirements = Requirement.query.all()

    # Convert the requirements to a list of dictionaries
    data = [req.to_dict() for req in requirements]

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Write the DataFrame to the Excel file using openpyxl engine
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Requirements")

    # Seek to the beginning of the file so it can be read
    excel_file.seek(0)

    # Send the file as a response with an appropriate content type and filename
    return send_file(
        excel_file,
        as_attachment=True,  # This will prompt automatic download
        download_name="requirements.xlsx",  # You can modify the filename as needed
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# Export a single requirement by ID to Excel (Download Single Requirement)
@requirements_bp.route("/requirements/<int:id>/export", methods=["GET"])
@jwt_required()  # Ensure the request has a valid JWT token
@role_required(roles=["Admin", "Super-Admin"])  # Make sure only authorized users can access this
def export_single_requirement_to_excel(id):
    # Query the requirement by ID from the database
    requirement = Requirement.query.get(id)

    if not requirement:
        return jsonify({"message": "Requirement not found"}), 404

    # Convert the requirement to a dictionary
    data = [requirement.to_dict()]

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Write the DataFrame to the Excel file using openpyxl engine
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Requirement")

    # Seek to the beginning of the file so it can be read
    excel_file.seek(0)

    # Send the file as a response with an appropriate content type and filename
    return send_file(
        excel_file,
        as_attachment=True,  # This will prompt automatic download
        download_name=f"requirement_{id}.xlsx",  # Custom filename for single requirement
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
