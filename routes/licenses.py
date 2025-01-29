import pandas as pd
from io import BytesIO
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from models import db, SoftwareLicense, LicenseAttribute, Joining
from requirements.auth import role_required
from sqlalchemy.orm import joinedload  # Importing joinedload to eagerly load relationships
from flask_cors import CORS

licenses_bp = Blueprint('licenses_bp', __name__)

CORS(
    licenses_bp,
    origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "https://cogs-354de766c1e7.herokuapp.com",
        "https://www.v97-cems.com"
    ],
    supports_credentials=True,
)

# Create Software License
@licenses_bp.route('/licenses', methods=['POST'])
@jwt_required()
@role_required(roles=['IT-Admin', 'Super-Admin'])
def create_license():
    data = request.get_json()

    # Ensure the employee exists
    employee = Joining.query.filter_by(employee_id=data['employee_id']).first()
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # Create new software license
    new_license = SoftwareLicense(employee_id=data['employee_id'])
    db.session.add(new_license)
    db.session.commit()

    # Add dynamic attributes if provided
    if 'attributes' in data:
        for attribute in data['attributes']:
            new_attribute = LicenseAttribute(
                license_id=new_license.license_id,
                attribute_name=attribute['attribute_name'],
                attribute_value=attribute['attribute_value']
            )
            db.session.add(new_attribute)
        db.session.commit()

    return jsonify({"message": "Software license created successfully", "license_id": new_license.license_id}), 201

# Get all Software Licenses (with attributes)
@licenses_bp.route('/licenses', methods=['GET'])
@jwt_required()
@role_required(roles=['IT-Admin', 'Super-Admin'])
def get_all_licenses():
    employee_id = request.args.get('employee_id')

    # Fetch licenses and include associated attributes using joinedload
    if employee_id:
        licenses = SoftwareLicense.query.filter_by(employee_id=employee_id).options(joinedload(SoftwareLicense.dynamic_attributes)).all()
    else:
        licenses = SoftwareLicense.query.options(joinedload(SoftwareLicense.dynamic_attributes)).all()

    if not licenses:
        return jsonify({"message": "No licenses found"}), 404

    result = [
        {
            "license_id": license.license_id,
            "employee_id": license.employee_id,
            "created_date": license.created_date,
            "last_modified_date": license.last_modified_date,
            "attributes": [
                {"attribute_name": attr.attribute_name, "attribute_value": attr.attribute_value}
                for attr in license.dynamic_attributes
            ]
        } for license in licenses
    ]
    return jsonify({"count": len(licenses), "licenses": result})

# Get a specific Software License by ID (with attributes)
@licenses_bp.route('/licenses/<int:license_id>', methods=['GET'])
@jwt_required()
@role_required(roles=['IT-Admin', 'Super-Admin'])
def get_license(license_id):
    # Fetch license and include associated attributes using joinedload
    license = SoftwareLicense.query.filter_by(license_id=license_id).options(joinedload(SoftwareLicense.dynamic_attributes)).first()

    if not license:
        return jsonify({"message": "License not found"}), 404

    license_data = {
        "license_id": license.license_id,
        "employee_id": license.employee_id,
        "created_date": license.created_date,
        "last_modified_date": license.last_modified_date,
        "attributes": [
            {
                "attribute_name": attr.attribute_name,
                "attribute_value": attr.attribute_value
            } for attr in license.dynamic_attributes
        ]
    }

    return jsonify(license_data), 200

# Update a Software License (update dynamic attributes)
@licenses_bp.route('/licenses/<int:license_id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['IT-Admin', 'Super-Admin'])
def update_license(license_id):
    data = request.get_json()

    # Find the license to update
    license = SoftwareLicense.query.filter_by(license_id=license_id).first()
    if not license:
        return jsonify({"message": "License not found"}), 404

    # Update dynamic attributes
    if 'attributes' in data:
        # Remove old attributes and add new ones
        LicenseAttribute.query.filter_by(license_id=license_id).delete()
        db.session.commit()

        for attribute in data['attributes']:
            new_attribute = LicenseAttribute(
                license_id=license_id,
                attribute_name=attribute['attribute_name'],
                attribute_value=attribute['attribute_value']
            )
            db.session.add(new_attribute)

    # Update the license record itself if needed
    if 'employee_id' in data:
        license.employee_id = data['employee_id']

    db.session.commit()

    return jsonify({"message": "Software license updated successfully"}), 200

# Delete a Software License
@licenses_bp.route('/licenses/<int:license_id>', methods=['DELETE'])
@jwt_required()
@role_required(roles=['IT-Admin', 'Super-Admin'])
def delete_license(license_id):
    license = SoftwareLicense.query.filter_by(license_id=license_id).first()

    if not license:
        return jsonify({"message": "License not found"}), 404

    # Delete related attributes
    LicenseAttribute.query.filter_by(license_id=license_id).delete()

    # Delete the license itself
    db.session.delete(license)
    db.session.commit()

    return jsonify({"message": "Software license deleted successfully"}), 200

# Export All Licenses to Excel
@licenses_bp.route('/licenses/export', methods=['GET'])
@jwt_required()
@role_required(roles=['IT-Admin', 'Super-Admin'])
def export_all_licenses():
    # Fetch all licenses with their attributes using joinedload
    licenses = SoftwareLicense.query.options(joinedload(SoftwareLicense.dynamic_attributes)).all()

    # If no licenses found
    if not licenses:
        return jsonify({"message": "No licenses found"}), 404

    # Prepare data for export
    data = []
    for license in licenses:
        for attr in license.dynamic_attributes:
            data.append({
                "license_id": license.license_id,
                "employee_id": license.employee_id,
                "created_date": license.created_date,
                "last_modified_date": license.last_modified_date,
                "attribute_name": attr.attribute_name,
                "attribute_value": attr.attribute_value
            })

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Write the DataFrame to the Excel file using openpyxl engine
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Licenses")

    # Seek to the beginning of the file so it can be read
    excel_file.seek(0)

    # Send the file as a response with an appropriate content type and filename
    return send_file(
        excel_file,
        as_attachment=True,
        download_name="licenses.xlsx",  # You can modify the filename as needed
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Export a Single License by ID to Excel
@licenses_bp.route('/licenses/<int:license_id>/export', methods=['GET'])
@jwt_required()
@role_required(roles=['IT-Admin', 'Super-Admin'])
def export_single_license(license_id):
    # Fetch the license by its ID and include associated attributes
    license = SoftwareLicense.query.filter_by(license_id=license_id).options(joinedload(SoftwareLicense.dynamic_attributes)).first()

    if not license:
        return jsonify({"message": "License not found"}), 404

    # Prepare data for export
    data = []
    for attr in license.dynamic_attributes:
        data.append({
            "license_id": license.license_id,
            "employee_id": license.employee_id,
            "created_date": license.created_date,
            "last_modified_date": license.last_modified_date,
            "attribute_name": attr.attribute_name,
            "attribute_value": attr.attribute_value
        })

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Write the DataFrame to the Excel file using openpyxl engine
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="License")

    # Seek to the beginning of the file so it can be read
    excel_file.seek(0)

    # Send the file as a response with an appropriate content type and filename
    return send_file(
        excel_file,
        as_attachment=True,
        download_name=f"license_{license_id}.xlsx",  # Dynamically naming the file based on license_id
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
