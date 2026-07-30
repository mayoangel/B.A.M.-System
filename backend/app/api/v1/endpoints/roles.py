from flask import Blueprint, request, jsonify
from app.core.database import get_db
from app.services.role_services import RoleService

roles_bp = Blueprint('roles', __name__, url_prefix='/roles')

@roles_bp.route('/', methods=['POST'])
def create_role():
    db = get_db()
    role_data = request.get_json() or {}
    try:
        service = RoleService(db)
        role = service.create_role(role_data)
        return jsonify({"message": f"Rol '{role.name}' creado con éxito.", "id": role.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@roles_bp.route('/<string:name>', methods=['GET'])
def get_role(name):
    db = get_db()
    try:
        service = RoleService(db)
        role = service.get_Role_Name(name)
        return jsonify({"id": role.id, "name": role.name, "description": role.description}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
@roles_bp.route('/', methods=['GET'])
def get_all_roles():
    db = get_db()
    try:
        service = RoleService(db)
        roles = service.list_all_roles()
        return jsonify([{
            "id": r.id,
            "name": r.name,
            "description": r.description
        } for r in roles]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@roles_bp.route('/<string:name>', methods=['PUT'])
def update_role(name):
    db = get_db()
    new_data = request.get_json() or {}
    try:
        service = RoleService(db)
        service.update_Role(name, new_data)
        return jsonify({"message": f"Rol '{name}' modificado correctamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@roles_bp.route('/<string:name>', methods=['DELETE'])
def delete_role(name):
    db = get_db()
    try:
        service = RoleService(db)
        service.delete_Role(name)
        return jsonify({"message": f"Rol '{name}' removido con éxito."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400