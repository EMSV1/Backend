from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required
from requirements.__init__ import db
from requirements.auth import role_required
from models import InterviewStatus
from datetime import datetime

# Blueprint setup
interview_bp = Blueprint('interview_bp', __name__)

# CORS configuration
CORS(
    interview_bp,
    origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "https://cogs-354de766c1e7.herokuapp.com",
        "https://www.v97-cems.com"
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
        candidate_name=data['candidate_name'],
        interviewer_name=data['interviewer_name'],
        interview_date=datetime.fromisoformat(data['interview_date']),
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
    return jsonify(interview_status.to_dict())

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
    interview_status.candidate_name = data.get('candidate_name', interview_status.candidate_name)
    interview_status.interviewer_name = data.get('interviewer_name', interview_status.interviewer_name)
    if 'interview_date' in data:
        interview_status.interview_date = datetime.fromisoformat(data['interview_date'])

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

# Add the to_dict method to the InterviewStatus class
def to_dict(self):
    return {
        'interview_id': self.interview_id,
        'requirement_id': self.requirement_id,
        'interview_status': self.interview_status,
        'interview_round': self.interview_round,
        'candidate_name': self.candidate_name,
        'interviewer_name': self.interviewer_name,
        'interview_date': self.interview_date.isoformat() if self.interview_date else None,
        'last_modified_date': self.last_modified_date.isoformat(),
    }

# Attach the to_dict method to the InterviewStatus class
InterviewStatus.to_dict = to_dict