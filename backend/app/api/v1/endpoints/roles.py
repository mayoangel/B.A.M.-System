from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.core.database import get_db
from app.services.role_service import RoleService
from app.schemas.role import RoleSchema

roles_bp = Blueprint('roles', __name__, url_prefix='/roles')
role_schema = RoleSchema()

@roles_bp.route('/', methods=['POST'])
def create_role():
    db = get_db()
    role_data = request.get_json() or {}
    try:
        role_schema.load(role_data)
    except ValidationError as err:
        return jsonify({"error": "Datos de rol inválidos.", "details": err.messages}), 400
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
        role_schema.load(new_data, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos de rol inválidos.", "details": err.messages}), 400
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