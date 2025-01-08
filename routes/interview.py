from flask import Blueprint, request, jsonify
from models import InterviewStatus
from requirements.__init__ import db
from requirements.auth import role_required

interview_bp = Blueprint('interview_bp', __name__)

# Only Admin can update interview status
@interview_bp.route('/interview_status/<int:id>', methods=['PUT'])
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

# Get interview status (Accessible to Admin only)
@interview_bp.route('/interview_status/<int:id>', methods=['GET'])
@role_required(roles=['Admin', 'Super-Admin'])
def get_interview_status(id):
    interview_status = InterviewStatus.query.get(id)
    if not interview_status:
        return jsonify({"message": "Interview status not found"}), 404
    return jsonify({
        'requirement_id': interview_status.requirement_id,
        'interview_status': interview_status.interview_status,
        'interview_round': interview_status.interview_round,
        'last_modified_date': interview_status.last_modified_date
    })
