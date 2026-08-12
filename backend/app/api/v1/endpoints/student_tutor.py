from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.core.database import get_db
from app.services.student_tutor_service import StudentTutorService
from app.schemas.student_tutor import StudentTutorSchema

student_tutor_bp = Blueprint('student_tutor', __name__, url_prefix='/tutor-assignments')
student_tutor_schema = StudentTutorSchema()

@student_tutor_bp.route('/', methods=['POST'])
def assign_tutor():
    db = get_db()
    assignment_data = request.get_json() or {}
    try:
        student_tutor_schema.load(assignment_data)
    except ValidationError as err:
        return jsonify({"error": "Datos de asignación inválidos.", "details": err.messages}), 400
    try:
        service = StudentTutorService(db)
        result = service.assign_tutor(assignment_data)
        return jsonify({"message": "Tutor asignado con éxito.", "id": result.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@student_tutor_bp.route('/Active/<int:student_id>', methods=['GET'])
def get_active_assignment(student_id):
    db = get_db()
    try:
        service = StudentTutorService(db)
        assignment = service.get_active_tutor_by_student(student_id)
        return jsonify({
            "id": assignment.id,
            "student_id": assignment.student_id,
            "employee_id": assignment.employee_id,
            "status": assignment.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404