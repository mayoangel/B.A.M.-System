from flask import Blueprint, request, jsonify, g
from app.services.employeecourse_services import EmployeeCourseService

employee_course_bp = Blueprint('employee_course', __name__)

@employee_course_bp.route('/assign', methods=['POST'])
def assign_course_to_employee():
    data = request.get_json() or {}
    employee_id = data.get("employee_id")
    course_id = data.get("course_id")
    try:
        service = EmployeeCourseService(g.db)
        service.assign_teacher_to_course(employee_id, course_id)
        return jsonify({"message": f"Profesor {employee_id} asignado al curso {course_id} con éxito."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@employee_course_bp.route('/unassign', methods=['DELETE'])
def unassign_course_from_employee():
    data = request.get_json() or {}
    employee_id = data.get("employee_id")
    course_id = data.get("course_id")
    try:
        service = EmployeeCourseService(g.db)
        service.remove_teacher_from_course(employee_id, course_id)
        return jsonify({"message": f"Se retiró al profesor {employee_id} del curso {course_id} exitosamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400