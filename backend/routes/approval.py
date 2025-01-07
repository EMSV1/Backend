from flask import Blueprint, request, jsonify
from models import RequirementApproval
from requirements.__init__ import db

from requirements.auth import role_required

approval_bp = Blueprint('approval_bp', __name__)

# Only Super Admin can approve or reject requirements
@approval_bp.route('/requirement_approval/<int:id>', methods=['PUT'])
@role_required(roles=['Super-Admin'])
def update_approval_status(id):
    data = request.json
    approval = RequirementApproval.query.get(id)
    if not approval:
        return jsonify({"message": "Approval not found"}), 404
    approval.approval_status = data.get('approval_status', approval.approval_status)
    approval.approved_by = data.get('approved_by', approval.approved_by)
    db.session.commit()
    return jsonify({"message": "Approval status updated successfully"})

# Get requirement approval details (Accessible to Admin only)
@approval_bp.route('/requirement_approval/<int:id>', methods=['GET'])
@role_required(roles=['Admin'])
def get_approval_status(id):
    approval = RequirementApproval.query.get(id)
    if not approval:
        return jsonify({"message": "Approval not found"}), 404
    return jsonify({
        'requirement_id': approval.requirement_id,
        'approval_status': approval.approval_status,
        'approved_by': approval.approved_by,
        'last_modified_date': approval.last_modified_date
    })
