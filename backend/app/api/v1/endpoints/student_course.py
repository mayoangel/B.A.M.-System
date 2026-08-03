from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.core.database import get_db
from app.services.student_course_service import StudentCoursesService
from app.schemas.student_courses import StudentCourseSchema

enrollments_bp = Blueprint('enrollments', __name__, url_prefix='/enrollments')
student_course_schema = StudentCourseSchema()

@enrollments_bp.route('/student/<int:student_id>', methods=['GET'])
def get_student_courses(student_id):
    db = get_db()
    try:
        service = StudentCoursesService(db)
        courses = service.get_courses_for_student(student_id)
        return jsonify([{"id": c.id, "name": c.name} for c in courses]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@enrollments_bp.route('/enroll', methods=['POST'])
def enroll_student():
    db = get_db()
    data = request.get_json() or {}
    try:
        student_course_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos.", "details": err.messages}), 400
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
    try:
        student_course_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos.", "details": err.messages}), 400
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    try:
        service = StudentCoursesService(db)
        service.remove_student_from_course(student_id, course_id)
        return jsonify({"message": f"Estudiante {student_id} dado de baja del curso {course_id} con éxito."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400