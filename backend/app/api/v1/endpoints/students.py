from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.core.database import get_db
from app.services.student_service import StudentService
from app.schemas.students import StudentSchema

students_bp = Blueprint('students', __name__, url_prefix='/students')
student_schema = StudentSchema()


def _serialize_student_detailed(s):
    """Incluye tutor y cursos embebidos; usado por la pantalla de
    administración de alumnos (tabla, filtros y modal de edición)."""
    return {
        "id": s.id,
        "id_student": s.id_student,
        "name": s.name,
        "lastname": s.lastname,
        "surename": s.surename,
        "date_of_birth": str(s.date_of_birth),
        "status": s.status,
        "id_parent": s.id_parent,
        "parent": {
            "id": s.parent.id,
            "name": s.parent.name,
            "lastname": s.parent.lastname,
            "email": s.parent.email,
            "phone": s.parent.phone,
        } if s.parent else None,
        "courses": [{"id": c.id, "name": c.name} for c in s.courses],
    }


@students_bp.route('/', methods=['POST'])
def register_student():
    db = get_db()
    student_data = request.get_json() or {}
    try:
        student_schema.load(student_data)
    except ValidationError as err:
        return jsonify({"error": "Datos de alumno inválidos.", "details": err.messages}), 400
    try:
        service = StudentService(db)
        result = service.register_student(student_data)
        return jsonify({
            "message": f"Alumno '{result.name}' registrado con éxito.",
            "id": result.id,
            "id_student": result.id_student,
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@students_bp.route('/', methods=['GET'])
def get_all_students():
    db = get_db()
    try:
        service = StudentService(db)
        students = service.list_all_students_detailed()
        return jsonify([_serialize_student_detailed(s) for s in students]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@students_bp.route('/id/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    db = get_db()
    try:
        service = StudentService(db)
        student = service.get_student_by_id(student_id)
        return jsonify(_serialize_student_detailed(student)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@students_bp.route('/id/<int:student_id>', methods=['PUT'])
def update_student_by_id(student_id):
    db = get_db()
    new_data = request.get_json() or {}
    try:
        student_schema.load(new_data, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos de alumno inválidos.", "details": err.messages}), 400
    try:
        service = StudentService(db)
        service.update_student_by_id(student_id, new_data)
        return jsonify({"message": "Expediente del alumno actualizado."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@students_bp.route('/id/<int:student_id>', methods=['DELETE'])
def delete_student_by_id(student_id):
    db = get_db()
    try:
        service = StudentService(db)
        service.delete_student_by_id(student_id)
        return jsonify({"message": "Alumno eliminado de la base de datos."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@students_bp.route('/course/<int:course_id>', methods=['GET'])
def get_students_by_course(course_id):
    db = get_db()
    try:
        service = StudentService(db)
        students = service.list_students_by_course(course_id)
        return jsonify([{
            "id": s.id,
            "id_student": s.id_student,
            "name": s.name,
            "lastname": s.lastname,
            "date_of_birth": str(s.date_of_birth),
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
            "date_of_birth": str(student.date_of_birth),
            "status": student.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@students_bp.route('/<string:name>', methods=['PUT'])
def update_student(name):
    db = get_db()
    new_data = request.get_json() or {}
    try:
        student_schema.load(new_data, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos de alumno inválidos.", "details": err.messages}), 400
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