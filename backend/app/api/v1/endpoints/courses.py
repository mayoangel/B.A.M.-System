from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from app.services.course_service import CourseService
from app.schemas.courses import CourseSchema

courses_bp = Blueprint('courses', __name__)
course_schema = CourseSchema()

def serialize_course(course):
    return {
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "category": course.category,
        "start_date": str(course.start_date),
        "end_date": str(course.end_date),
        "time_duration": course.time_duration,
        "days_of_week": course.days_of_week,
        "status": course.status,
    }

@courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json() or {}
    try:
        course_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos de curso inválidos.", "details": err.messages}), 400
    try:
        service = CourseService(g.db)
        result = service.register_course(data)
        return jsonify({"message": f"Curso '{result.name}' creado exitosamente.", "id": result.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@courses_bp.route('/', methods=['GET'])
def get_all_courses():
    try:
        service = CourseService(g.db)
        courses = service.get_all_courses()
        return jsonify([serialize_course(c) for c in courses]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@courses_bp.route('/active', methods=['GET'])
def get_active_courses():
    try:
        service = CourseService(g.db)
        courses = service.get_active_courses()
        return jsonify([serialize_course(c) for c in courses]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Cubre errores no previstos (ej. base de datos no disponible) para que
        # el frontend siempre reciba una respuesta JSON con encabezados CORS,
        # en vez de una página de error que el navegador bloquearía.
        return jsonify({"error": f"No se pudieron obtener los cursos activos: {e}"}), 500

@courses_bp.route('/<string:name>', methods=['GET'])
def get_course(name):
    try:
        service = CourseService(g.db)
        course = service.get_course_by_name(name)
        return jsonify([serialize_course(course)]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@courses_bp.route('/<string:name>', methods=['DELETE'])
def delete_course(name):
    try:
        service = CourseService(g.db)
        service.delete_course(name)
        return jsonify({"message": f"Curso '{name}' eliminado correctamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400