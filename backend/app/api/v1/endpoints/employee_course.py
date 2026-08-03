from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from app.services.employee_course_service import EmployeeCourseService
from app.schemas.employee_course import EmployeeCourseSchema
from app.core.permissions import admin_required, authenticated_required

employee_course_bp = Blueprint('employee_course', __name__)
employee_course_schema = EmployeeCourseSchema()

@employee_course_bp.route('/course/<int:course_id>', methods=['GET'])
@authenticated_required
def get_employees_by_course(course_id):
    """Empleados/docentes asignados a un curso (usado para mostrar el maestro
    titular en la pantalla de Pase de Lista)."""
    try:
        service = EmployeeCourseService(g.db)
        employees = service.get_employees_for_course(course_id)
        return jsonify([{
            "id": e.id,
            "id_employee": e.id_employee,
            "name": e.name,
            "lastname": e.lastname,
            "email": e.email,
        } for e in employees]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@employee_course_bp.route('/assign', methods=['POST'])
@admin_required
def assign_course_to_employee():
    data = request.get_json() or {}
    try:
        employee_course_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos.", "details": err.messages}), 400
    employee_id = data.get("employee_id")
    course_id = data.get("course_id")
    try:
        service = EmployeeCourseService(g.db)
        service.assign_course_to_employee(employee_id, course_id)
        return jsonify({"message": f"Profesor {employee_id} asignado al curso {course_id} con éxito."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@employee_course_bp.route('/unassign', methods=['DELETE'])
@admin_required
def unassign_course_from_employee():
    data = request.get_json() or {}
    try:
        employee_course_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos.", "details": err.messages}), 400
    employee_id = data.get("employee_id")
    course_id = data.get("course_id")
    try:
        service = EmployeeCourseService(g.db)
        service.remove_course_from_employee(employee_id, course_id)
        return jsonify({"message": f"Se retiró al profesor {employee_id} del curso {course_id} exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400