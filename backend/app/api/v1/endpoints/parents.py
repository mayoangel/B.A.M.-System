from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.core.database import get_db
from app.services.parents_service import ParentService
from app.schemas.parents import ParentSchema

parents_bp = Blueprint('parents', __name__, url_prefix='/parents')
parent_schema = ParentSchema()

@parents_bp.route('/', methods=['POST'])
def create_parent():
    db = get_db()
    parent_data = request.get_json() or {}
    try:
        parent_schema.load(parent_data)
    except ValidationError as err:
        return jsonify({"error": "Datos de tutor inválidos.", "details": err.messages}), 400
    try:
        service = ParentService(db)
        result = service.register_parent(parent_data)
        return jsonify({"message": f"Tutor '{result.name}' registrado.", "id": result.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@parents_bp.route('/id/<int:parent_id>', methods=['GET'])
def get_parent_by_id(parent_id):
    db = get_db()
    try:
        service = ParentService(db)
        parent = service.get_parent_by_id(parent_id)
        return jsonify({
            "id": parent.id,
            "name": parent.name,
            "lastname": parent.lastname,
            "surename": parent.surename,
            "email": parent.email,
            "phone": parent.phone,
            "dir_street": parent.dir_street,
            "dir_col": parent.dir_col,
            "dir_num": parent.dir_num,
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@parents_bp.route('/id/<int:parent_id>', methods=['PUT'])
def update_parent_by_id(parent_id):
    db = get_db()
    new_data = request.get_json() or {}
    try:
        parent_schema.load(new_data, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos de tutor inválidos.", "details": err.messages}), 400
    try:
        service = ParentService(db)
        service.update_parent_by_id(parent_id, new_data)
        return jsonify({"message": "Tutor actualizado con éxito."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@parents_bp.route('/<string:name>', methods=['GET'])
def get_parent(name):
    db = get_db()
    try:
        service = ParentService(db)
        parent = service.get_parent_by_name(name)
        return jsonify({"id": parent.id, "name": parent.name, "email": parent.email}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@parents_bp.route('/<string:name>', methods=['PUT'])
def update_parent(name):
    db = get_db()
    new_data = request.get_json() or {}
    try:
        parent_schema.load(new_data, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos de tutor inválidos.", "details": err.messages}), 400
    try:
        service = ParentService(db)
        service.update_parent(name, new_data)
        return jsonify({"message": f"Tutor '{name}' actualizado con éxito."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@parents_bp.route('/<string:name>', methods=['DELETE'])
def delete_parent(name):
    db = get_db()
    try:
        service = ParentService(db)
        service.delete_parent(name)
        return jsonify({"message": f"Tutor '{name}' eliminado con éxito."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400