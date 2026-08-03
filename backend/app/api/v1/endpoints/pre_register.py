from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.core.database import get_db
from app.services.pre_register_service import PreRegisterService
from app.schemas.pre_register import PreRegisterSchema

pre_register_bp = Blueprint('pre_register', __name__, url_prefix='/pre-register')
pre_register_schema = PreRegisterSchema()

@pre_register_bp.route('/', methods=['POST'])
def create_pre_register():
    db = get_db()
    pre_data = request.get_json() or {}
    try:
        pre_register_schema.load(pre_data)
    except ValidationError as err:
        return jsonify({"error": "Datos de pre-registro inválidos.", "details": err.messages}), 400
    try:
        service = PreRegisterService(db)
        result = service.create_pre_register(pre_data)
        return jsonify({"message": "Pre-registro completado con éxito.", "id": result.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@pre_register_bp.route('/', methods=['GET'])
def get_all_pre_registers():
    db = get_db()
    service = PreRegisterService(db)
    records = service.get_all_pre_registers()
    return jsonify([{"id": r.id, "name": r.name, "lastname": r.lastname, "surename": r.surename, "course_id": r.course_id} for r in records]), 200

@pre_register_bp.route('/<int:pre_id>', methods=['GET'])
def get_pre_register(pre_id):
    db = get_db()
    try:
        service = PreRegisterService(db)
        record = service.get_pre_register_by_id(pre_id)
        return jsonify({"id": record.id, "name": record.name, "lastname": record.lastname, "surename": record.surename, "course_id": record.course_id}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@pre_register_bp.route('/course/<int:course_id>', methods=['GET'])
def get_pre_registers_by_course(course_id):
    db = get_db()
    service = PreRegisterService(db)
    records = service.get_pre_registers_by_course(course_id)
    return jsonify([{"id": r.id, "name": r.name, "lastname": r.lastname, "surename": r.surename, "course_id": r.course_id} for r in records]), 200

@pre_register_bp.route('/<int:pre_id>', methods=['DELETE'])
def delete_pre_register(pre_id):
    db = get_db()
    try:
        service = PreRegisterService(db)
        service.delete_pre_register(pre_id)
        return jsonify({"message": f"Pre-registro con ID {pre_id} eliminado."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400