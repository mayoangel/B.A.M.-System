from flask import Blueprint, request, jsonify
from app.core.database import get_db
from app.services.parents_services import ParentService

parents_bp = Blueprint('parents', __name__, url_prefix='/parents')

@parents_bp.route('/', methods=['POST'])
def create_parent():
    db = get_db()
    parent_data = request.get_json() or {}
    try:
        service = ParentService(db)
        result = service.register_parent(parent_data)
        return jsonify({"message": f"Tutor '{result.name}' registrado.", "id": result.id}), 201
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