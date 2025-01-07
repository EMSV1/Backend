from flask import Blueprint, request, jsonify
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
@role_required(roles=["IT-Admin"])
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


@assets_bp.route("/it_assets", methods=["GET"])
@jwt_required()
@role_required(roles=["IT-Admin"])
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
    return jsonify(assets_list), 200


@assets_bp.route("/it_assets/<int:id>", methods=["GET"])
@jwt_required()
@role_required(roles=["IT-Admin"])
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
@role_required(roles=["IT-Admin"])
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
@role_required(roles=["IT-Admin"])
def delete_it_asset(id):
    asset = ITAssets.query.get(id)
    if not asset:
        return jsonify({"message": "IT asset not found"}), 404

    db.session.delete(asset)
    db.session.commit()
    return jsonify({"message": "IT asset deleted successfully"}), 200
