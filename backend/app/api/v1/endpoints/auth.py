from flask import Blueprint, request, jsonify, g

from app.services.auth_service import AuthService
from app.core.permissions import admin_required, authenticated_required

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Correo y contraseña son obligatorios."
        }), 400

    service = AuthService(g.db)

    result = service.login(
        email,
        password
    )

    if not result:
        return jsonify({
            "error": "Credenciales inválidas."
        }), 401

    return jsonify(result), 200


@auth_bp.route(
    "/me",
    methods=["GET"]
)
@authenticated_required
def me():

    service = AuthService(g.db)

    profile = service.get_profile(g.current_actor)

    if not profile:
        return jsonify({
            "error": "Usuario no encontrado"
        }), 404

    return jsonify(profile)


@auth_bp.route(
    "/change-role",
    methods=["PUT"]
)
@admin_required
def change_role():

    data = request.get_json() or {}

    employee_id = data.get(
        "employee_id"
    )

    new_role_id = data.get(
        "role_id"
    )

    service = AuthService(g.db)

    try:
        service.change_role(
            g.current_actor["role"],
            employee_id,
            new_role_id
        )
    except PermissionError as e:
        return jsonify({
            "error": str(e)
        }), 403
    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400
    except LookupError as e:
        return jsonify({
            "error": str(e)
        }), 404

    return jsonify({
        "message":
        "Rol actualizado correctamente"
    })


@auth_bp.route(
    "/logout",
    methods=["POST"]
)
@authenticated_required
def logout():

    return jsonify({
        "message": "Sesión cerrada correctamente"
    }), 200
