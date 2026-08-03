from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from app.services.employee_service import EmployeeService
from app.schemas.employees import EmployeeSchema

employees_bp = Blueprint('employees', __name__)
employee_schema = EmployeeSchema()

@employees_bp.route('/', methods=['POST'])
def register_employee():
    data = request.get_json() or {}
    try:
        employee_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos de empleado inválidos.", "details": err.messages}), 400
    try:
        service = EmployeeService(g.db)
        result = service.register_employee(data)
        return jsonify({"message": f"Empleado '{result.name}' contratado/registrado.", "id": result.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@employees_bp.route('/', methods=['GET'])
def get_all_employees():
    try:
        service = EmployeeService(g.db)
        employees = service.list_all_employees()
        return jsonify([{
            "id": emp.id, 
            "id_employee": emp.id_employee,
            "name": emp.name, 
            "lastname": emp.lastname,
            "email": emp.email, 
            "role_id": emp.role_id,
            "status": emp.status
        } for emp in employees]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employees_bp.route('/role/<int:role_id>', methods=['GET'])
def get_employees_by_role(role_id):
    try:
        service = EmployeeService(g.db)
        employees = service.get_employees_by_role(role_id)
        return jsonify([{
            "id": emp.id, 
            "id_employee": emp.id_employee,
            "name": emp.name, 
            "lastname": emp.lastname,
            "email": emp.email, 
            "role_id": emp.role_id,
            "status": emp.status
        } for emp in employees]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@employees_bp.route('/<string:name>', methods=['GET'])
def get_employee(name):
    try:
        service = EmployeeService(g.db)
        employee = service.get_employee_by_name(name)
        return jsonify({
            "id": employee.id, 
            "id_employee": employee.id_employee,
            "name": employee.name, 
            "lastname": employee.lastname,
            "email": employee.email, 
            "role_id": employee.role_id,
            "status": employee.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404