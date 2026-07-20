from flask import Blueprint, request, jsonify
from app.core.database import get_db
from app.services.student_services import StudentService

students_bp = Blueprint('students', __name__, url_prefix='/students')

@students_bp.route('/', methods=['POST'])
def register_student():
    db = get_db()
    student_data = request.get_json() or {}
    try:
        service = StudentService(db)
        result = service.register_student(student_data)
        return jsonify({"message": f"Alumno '{result.name}' registrado con éxito.", "id": result.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@students_bp.route('/', methods=['GET'])
def get_all_students():
    db = next(get_db())
    try:
        service = StudentService(db)
        students = service.list_all_students()
        return jsonify([{
            "id": s.id,
            "id_student": s.id_student,
            "name": s.name,
            "lastname": s.lastname,
            "email": s.email,
            "status": s.status
        } for s in students]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@students_bp.route('/course/<int:course_id>', methods=['GET'])
def get_students_by_course(course_id):
    db = next(get_db())
    try:
        service = StudentService(db)
        students = service.list_students_by_course(course_id)
        return jsonify([{
            "id": s.id,
            "id_student": s.id_student,
            "name": s.name,
            "lastname": s.lastname,
            "email": s.email,
            "status": s.status
        } for s in students]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@students_bp.route('/<string:name>', methods=['GET'])
def get_student(name):
    db = get_db()
    try:
        service = StudentService(db)
        student = service.get_student_by_name(name)
        return jsonify({
            "id": student.id,
            "id_student": student.id_student,
            "name": student.name,
            "lastname": student.lastname,
            "email": student.email,
            "status": student.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@students_bp.route('/<string:name>', methods=['PUT'])
def update_student(name):
    db = get_db()
    new_data = request.get_json() or {}
    try:
        service = StudentService(db)
        service.update_student(name, new_data)
        return jsonify({"message": f"Expediente del alumno '{name}' actualizado."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@students_bp.route('/<string:name>', methods=['DELETE'])
def delete_student(name):
    db = get_db()
    try:
        service = StudentService(db)
        service.delete_student(name)
        return jsonify({"message": f"Alumno '{name}' eliminado de la base de datos."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400