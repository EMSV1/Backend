from flask import Blueprint, request, jsonify
from models import InterviewStatus
from requirements.__init__ import db
from requirements.auth import role_required
from flask_jwt_extended import jwt_required
from flask_cors import CORS

interview_bp = Blueprint('interview_bp', __name__)

CORS(
    interview_bp,
    origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "https://cogs-354de766c1e7.herokuapp.com",
    ],
    supports_credentials=True,
)

# Create a new interview status
@interview_bp.route('/interview', methods=['POST'])
@jwt_required()
@role_required(roles=['Admin', 'Super-Admin'])
def create_interview_status():
    data = request.json
    new_interview_status = InterviewStatus(
        requirement_id=data['requirement_id'],
        interview_status=data['interview_status'],
        interview_round=data['interview_round'],
    )
    db.session.add(new_interview_status)
    db.session.commit()
    return jsonify({"message": "Interview status created successfully"}), 201

# Get a specific interview status by ID
@interview_bp.route('/interview/<int:id>', methods=['GET'])
@jwt_required()
@role_required(roles=['Admin', 'Super-Admin'])
def get_interview_status(id):
    interview_status = InterviewStatus.query.get(id)
    if not interview_status:
        return jsonify({"message": "Interview status not found"}), 404
    return jsonify({
        'requirement_id': interview_status.requirement_id,
        'interview_status': interview_status.interview_status,
        'interview_round': interview_status.interview_round,
        'last_modified_date': interview_status.last_modified_date.isoformat(),
    })

# Get all interview statuses
@interview_bp.route('/interview', methods=['GET'])
@jwt_required()
@role_required(roles=['Admin', 'Super-Admin'])
def get_all_interview_statuses():
    interview_statuses = InterviewStatus.query.all()
    result = [status.to_dict() for status in interview_statuses]
    return jsonify(result)

# Update an existing interview status
@interview_bp.route('/interview/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(roles=['Admin', 'Super-Admin'])
def update_interview_status(id):
    data = request.json
    interview_status = InterviewStatus.query.get(id)
    if not interview_status:
        return jsonify({"message": "Interview status not found"}), 404

    interview_status.interview_status = data.get('interview_status', interview_status.interview_status)
    interview_status.interview_round = data.get('interview_round', interview_status.interview_round)
    db.session.commit()
    return jsonify({"message": "Interview status updated successfully"})

# Delete an interview status
@interview_bp.route('/interview/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(roles=['Admin', 'Super-Admin'])
def delete_interview_status(id):
    interview_status = InterviewStatus.query.get(id)
    if not interview_status:
        return jsonify({"message": "Interview status not found"}), 404
    db.session.delete(interview_status)
    db.session.commit()
    return jsonify({"message": "Interview status deleted successfully"})

# Utility function for converting an InterviewStatus object to a dictionary
def to_dict(self):
    return {
        'requirement_id': self.requirement_id,
        'interview_status': self.interview_status,
        'interview_round': self.interview_round,
        'last_modified_date': self.last_modified_date.isoformat(),
    }

# Add the to_dict method to the InterviewStatus class
InterviewStatus.to_dict = to_dict
