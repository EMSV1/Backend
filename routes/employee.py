# from flask import Blueprint, request, jsonify
# from requirements.__init__ import db
# from models import EmployeeManagement

# employee_bp = Blueprint('employee_bp', __name__)

# @employee_bp.route('/employee', methods=['POST'])
# def create_employee():
#     data = request.json
#     new_employee = EmployeeManagement(
#         first_name=data['first_name'],
#         last_name=data['last_name'],
#         employment_status=data['employment_status']
#     )
#     db.session.add(new_employee)
#     db.session.commit()
#     return jsonify({"message": "Employee created successfully"}), 201

# @employee_bp.route('/employee/<int:id>', methods=['GET'])
# def get_employee(id):
#     employee = EmployeeManagement.query.get(id)
#     if not employee:
#         return jsonify({"message": "Employee not found"}), 404
#     return jsonify({
#         "employee_id": employee.employee_id,
#         "first_name": employee.first_name,
#         "last_name": employee.last_name,
#         "employment_status": employee.employment_status
#     })

# @employee_bp.route('/employee/<int:id>', methods=['PUT'])
# def update_employee(id):
#     data = request.json
#     employee = EmployeeManagement.query.get(id)
#     if not employee:
#         return jsonify({"message": "Employee not found"}), 404
#     employee.first_name = data.get('first_name', employee.first_name)
#     employee.last_name = data.get('last_name', employee.last_name)
#     employee.employment_status = data.get('employment_status', employee.employment_status)
#     db.session.commit()
#     return jsonify({"message": "Employee updated successfully"})

# @employee_bp.route('/employee/<int:id>', methods=['DELETE'])
# def delete_employee(id):
#     employee = EmployeeManagement.query.get(id)
#     if not employee:
#         return jsonify({"message": "Employee not found"}), 404
#     db.session.delete(employee)
#     db.session.commit()
#     return jsonify({"message": "Employee deleted successfully"})
