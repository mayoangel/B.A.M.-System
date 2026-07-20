

######### LO AGREGUE PARA EL REQUIRIEMIENTO 5   ##########


from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if claims.get("role_id") != 1:
            return jsonify({
                "message": "Acceso solo para administradores"
            }), 403

        return fn(*args, **kwargs)

    return wrapper


def professor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if claims.get("role_id") not in [1, 2]:
            return jsonify({
                "message": "Acceso solo para profesores"
            }), 403

        return fn(*args, **kwargs)

    return wrapper


def prefect_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if claims.get("role_id") not in [1, 3]:
            return jsonify({
                "message": "Acceso solo para prefectos"
            }), 403

        return fn(*args, **kwargs)

    return wrapper