

######### LO AGREGUE PARA EL REQUIRIEMIENTO 5   ##########

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import g
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    service = AuthService(g.db)

    result = service.login(
        email,
        password
    )

    if not result:
        return jsonify({
            "message": "Credenciales inválidas"
        }), 401

    return jsonify(result), 200


@auth_bp.route(
    "/me",
    methods=["GET"]
)
@jwt_required()
def me():

    employee_id = get_jwt_identity()

    service = AuthService(g.db)

    profile = service.get_profile(employee_id)

    if not profile:
        return jsonify({
            "message": "Usuario no encontrado"
        }), 404

    return jsonify(profile)


@auth_bp.route(
    "/change-role",
    methods=["PUT"]
)
@jwt_required()
def change_role():

    claims = get_jwt()

    data = request.get_json()

    employee_id = data.get(
        "employee_id"
    )

    new_role_id = data.get(
        "role_id"
    )

    service = AuthService(g.db)

    try:
        service.change_role(
            claims.get("role_id"),
            employee_id,
            new_role_id
        )
    except PermissionError as e:
        return jsonify({
            "message": str(e)
        }), 403
    except ValueError as e:
        return jsonify({
            "message": str(e)
        }), 400
    except LookupError as e:
        return jsonify({
            "message": str(e)
        }), 404

    return jsonify({
        "message":
        "Rol actualizado correctamente"
    })


##ESTE es para que el frontend sepa que mostrar en el menu dependieno su rol
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    claims = get_jwt()

    return {
        "employee_id": get_jwt_identity(),
        "name": claims.get("name"),
        "role_id": claims.get("role_id")
    }, 200



@auth_bp.route(
    "/logout",
    methods=["POST"]
)
@jwt_required()
def logout():

    return jsonify({
        "message": "Sesión cerrada correctamente"
    }), 200