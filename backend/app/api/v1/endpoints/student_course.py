from flask import Blueprint, request, jsonify
from app.core.database import get_db
from app.services.studentcourse_services import StudentCoursesService

enrollments_bp = Blueprint('enrollments', __name__, url_prefix='/enrollments')

@enrollments_bp.route('/enroll', methods=['POST'])
def enroll_student():
    db = get_db()
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    try:
        service = StudentCoursesService(db)
        service.enroll_student_in_course(student_id, course_id)
        return jsonify({"message": f"Estudiante {student_id} inscrito en curso {course_id} con éxito."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@enrollments_bp.route('/unenroll', methods=['DELETE'])
def unenroll_student():
    db = get_db()
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    try:
        service = StudentCoursesService(db)
        service.remove_student_from_course(student_id, course_id)
        return jsonify({"message": f"Estudiante {student_id} dado de baja del curso {course_id} con éxito."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400