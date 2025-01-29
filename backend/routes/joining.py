import pandas as pd
from io import BytesIO
from flask import Blueprint, request, jsonify, send_file
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
        "https://www.v97-cems.com"
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

# Get all joining records
@joining_bp.route("/joining", methods=["GET"])
@jwt_required()
@role_required(roles=["HR", "Super-Admin"])
def get_all_joining():
    joinings = Joining.query.all()
    return jsonify({"count": len(joinings), "joinings": [joi.to_dict() for joi in joinings]})

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

# Export All Joining Records to Excel
@joining_bp.route('/joining/export', methods=['GET'])
@jwt_required()
@role_required(roles=["HR", "Super-Admin"])
def export_all_joining():
    # Fetch all joining records
    joinings = Joining.query.all()

    # If no joining records found
    if not joinings:
        return jsonify({"message": "No joining records found"}), 404

    # Prepare data for export
    data = []
    for joining in joinings:
        data.append({
            "employee_id": joining.employee_id,
            "first_name": joining.first_name,
            "last_name": joining.last_name,
            "emp_email_id": joining.emp_email_id,
            "employee_address": joining.employee_address,
            "business_unit": joining.business_unit,
            "business_title": joining.business_title,
            "resource_type": joining.resource_type,
            "contact_number": joining.contact_number,
            "reporting_manager": joining.reporting_manager,
            "employment_status": joining.employment_status,
            "created_date": joining.created_date,
            "last_modified_date": joining.last_modified_date
        })

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Write the DataFrame to the Excel file using openpyxl engine
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Joinings")

    # Seek to the beginning of the file so it can be read
    excel_file.seek(0)

    # Send the file as a response with an appropriate content type and filename
    return send_file(
        excel_file,
        as_attachment=True,
        download_name="joinings.xlsx",  # You can modify the filename as needed
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Export a Single Joining Record by ID to Excel
@joining_bp.route('/joining/<int:id>/export', methods=['GET'])
@jwt_required()
@role_required(roles=["HR", "Super-Admin"])
def export_single_joining(id):
    # Fetch the joining record by its ID
    joining = Joining.query.get(id)

    if not joining:
        return jsonify({"message": "Joining not found"}), 404

    # Prepare data for export
    data = [{
        "employee_id": joining.employee_id,
        "first_name": joining.first_name,
        "last_name": joining.last_name,
        "emp_email_id": joining.emp_email_id,
        "employee_address": joining.employee_address,
        "business_unit": joining.business_unit,
        "business_title": joining.business_title,
        "resource_type": joining.resource_type,
        "contact_number": joining.contact_number,
        "reporting_manager": joining.reporting_manager,
        "employment_status": joining.employment_status,
        "created_date": joining.created_date,
        "last_modified_date": joining.last_modified_date
    }]

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Write the DataFrame to the Excel file using openpyxl engine
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Joining")

    # Seek to the beginning of the file so it can be read
    excel_file.seek(0)

    # Send the file as a response with an appropriate content type and filename
    return send_file(
        excel_file,
        as_attachment=True,
        download_name=f"joining_{id}.xlsx",  # Dynamically naming the file based on joining ID
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
