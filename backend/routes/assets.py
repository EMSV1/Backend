import pandas as pd
from io import BytesIO
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from models import ITAssets
from requirements.__init__ import db
from requirements.auth import role_required
from flask_cors import CORS

assets_bp = Blueprint("assets_bp", __name__)

CORS(
    assets_bp,
    origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3000",
        "https://cogs-354de766c1e7.herokuapp.com"
    ],
    supports_credentials=True,
)


@assets_bp.route("/it_assets", methods=["POST"])
@jwt_required()
@role_required(roles=["IT-Admin", "Super-Admin"])
def create_it_assets():
    data = request.json
    required_fields = [
        "employee_id",
        "laptop",
        "monitor",
        "wired_keyboard",
        "wired_mouse",
        "wireless_mouse",
        "airtel_dongle",
        "id_card",
        "employment_status",
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 422

    new_asset = ITAssets(**data)
    db.session.add(new_asset)
    db.session.commit()
    return jsonify({"message": "IT asset created successfully"}), 201


# Get all IT assets
@assets_bp.route("/it_assets", methods=["GET"])
@jwt_required()
@role_required(roles=["IT-Admin", "Super-Admin"])
def get_all_it_assets():
    assets = ITAssets.query.all()
    assets_list = [
        {
            "asset_id": asset.asset_id,
            "employee_id": asset.employee_id,
            "laptop": asset.laptop,
            "monitor": asset.monitor,
            "wired_keyboard": asset.wired_keyboard,
            "wired_mouse": asset.wired_mouse,
            "wireless_mouse": asset.wireless_mouse,
            "airtel_dongle": asset.airtel_dongle,
            "id_card": asset.id_card,
            "employment_status": asset.employment_status,
            "created_date": asset.created_date,
            "last_modified_date": asset.last_modified_date,
        }
        for asset in assets
    ]
    return jsonify({"count": len(assets), "assets": assets_list})


@assets_bp.route("/it_assets/<int:id>", methods=["GET"])
@jwt_required()
@role_required(roles=["IT-Admin", "Super-Admin"])
def get_it_asset(id):
    asset = ITAssets.query.get(id)
    if not asset:
        return jsonify({"message": "IT asset not found"}), 404
    return jsonify(
        {
            "asset_id": asset.asset_id,
            "employee_id": asset.employee_id,
            "laptop": asset.laptop,
            "monitor": asset.monitor,
            "wired_keyboard": asset.wired_keyboard,
            "wired_mouse": asset.wired_mouse,
            "wireless_mouse": asset.wireless_mouse,
            "airtel_dongle": asset.airtel_dongle,
            "id_card": asset.id_card,
            "employment_status": asset.employment_status,
            "created_date": asset.created_date,
            "last_modified_date": asset.last_modified_date,
        }
    )


@assets_bp.route("/it_assets/<int:id>", methods=["PUT"])
@jwt_required()
@role_required(roles=["IT-Admin", "Super-Admin"])
def update_it_asset(id):
    data = request.json
    asset = ITAssets.query.get(id)
    if not asset:
        return jsonify({"message": "IT asset not found"}), 404

    for key, value in data.items():
        setattr(asset, key, value)

    db.session.commit()
    return jsonify({"message": "IT asset updated successfully"}), 200


@assets_bp.route("/it_assets/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required(roles=["IT-Admin", "Super-Admin"])
def delete_it_asset(id):
    asset = ITAssets.query.get(id)
    if not asset:
        return jsonify({"message": "IT asset not found"}), 404

    db.session.delete(asset)
    db.session.commit()
    return jsonify({"message": "IT asset deleted successfully"}), 200

# Export all IT assets to Excel
@assets_bp.route('/it_assets/export', methods=['GET'])
@jwt_required()
@role_required(roles=["IT-Admin", "Super-Admin"])
def export_all_it_assets():
    # Fetch all IT assets
    assets = ITAssets.query.all()

    # If no IT assets found
    if not assets:
        return jsonify({"message": "No IT assets found"}), 404

    # Prepare data for export
    data = []
    for asset in assets:
        data.append({
            "asset_id": asset.asset_id,
            "employee_id": asset.employee_id,
            "laptop": asset.laptop,
            "monitor": asset.monitor,
            "wired_keyboard": asset.wired_keyboard,
            "wired_mouse": asset.wired_mouse,
            "wireless_mouse": asset.wireless_mouse,
            "airtel_dongle": asset.airtel_dongle,
            "id_card": asset.id_card,
            "employment_status": asset.employment_status,
            "created_date": asset.created_date,
            "last_modified_date": asset.last_modified_date
        })

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Write the DataFrame to the Excel file using openpyxl engine
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="IT Assets")

    # Seek to the beginning of the file so it can be read
    excel_file.seek(0)

    # Send the file as a response with an appropriate content type and filename
    return send_file(
        excel_file,
        as_attachment=True,
        download_name="it_assets.xlsx",  # You can modify the filename as needed
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Export a specific IT asset by ID to Excel
@assets_bp.route('/it_assets/<int:id>/export', methods=['GET'])
@jwt_required()
@role_required(roles=["IT-Admin", "Super-Admin"])
def export_single_it_asset(id):
    # Fetch the IT asset by its ID
    asset = ITAssets.query.get(id)

    if not asset:
        return jsonify({"message": "IT asset not found"}), 404

    # Prepare data for export
    data = [{
        "asset_id": asset.asset_id,
        "employee_id": asset.employee_id,
        "laptop": asset.laptop,
        "monitor": asset.monitor,
        "wired_keyboard": asset.wired_keyboard,
        "wired_mouse": asset.wired_mouse,
        "wireless_mouse": asset.wireless_mouse,
        "airtel_dongle": asset.airtel_dongle,
        "id_card": asset.id_card,
        "employment_status": asset.employment_status,
        "created_date": asset.created_date,
        "last_modified_date": asset.last_modified_date
    }]

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO object to store the Excel file in memory
    excel_file = BytesIO()

    # Write the DataFrame to the Excel file using openpyxl engine
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="IT Asset")

    # Seek to the beginning of the file so it can be read
    excel_file.seek(0)

    # Send the file as a response with an appropriate content type and filename
    return send_file(
        excel_file,
        as_attachment=True,
        download_name=f"it_asset_{id}.xlsx",  # Dynamically naming the file based on asset ID
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
