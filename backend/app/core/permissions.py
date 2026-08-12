"""Autorización basada en roles (RBAC) a partir de los claims del JWT.

El token se emite en `AuthService.login` con dos claims clave:
  - `role`: "admin" | "docente" | "tutor"
  - `actor_type`: "employee" | "parent" (tabla de origen del actor)

Los decoradores de este módulo SOLO controlan el acceso al endpoint (¿puede
este rol entrar aquí?). El FILTRADO de datos (ej. un docente solo ve a los
alumnos de sus propios cursos, un tutor solo ve a sus propios hijos) es
responsabilidad de la capa de `services/`, que recibe al actor autenticado
(ver `get_current_actor`) y decide qué consultas ejecutar o qué excepción
lanzar. Esto respeta la separación de capas de CLAUDE.md: la presentación
(`api/`) no debe contener reglas de negocio.
"""
from functools import wraps

from flask import g, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

ROLE_ADMIN = "admin"
ROLE_DOCENTE = "docente"
ROLE_TUTOR = "tutor"


def get_current_actor() -> dict:
    """Actor autenticado extraído del JWT vigente: `id` numérico (de la
    tabla `employees` o `parents`, según `actor_type`), `role` y `name`.
    Solo debe llamarse dentro de una vista ya protegida por alguno de los
    decoradores de este módulo (requieren un JWT válido)."""
    claims = get_jwt()
    return {
        "id": int(get_jwt_identity()),
        "role": claims.get("role"),
        "actor_type": claims.get("actor_type"),
        "name": claims.get("name"),
    }


def roles_required(*allowed_roles):
    """Exige un JWT válido cuyo claim `role` esté en `allowed_roles`.

    Además, deja el actor autenticado disponible en `g.current_actor` para
    que el endpoint lo reenvíe a la capa de servicios y esta aplique el
    filtrado de datos correspondiente a su rol.
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            actor = get_current_actor()
            if actor["role"] not in allowed_roles:
                return jsonify({"error": "No tienes permisos para acceder a este recurso."}), 403
            g.current_actor = actor
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# Combinaciones de conveniencia usadas por los endpoints, alineadas con las
# reglas de negocio de RBAC:
#   - Administrador: acceso total (CRUD) a alumnos, docentes, cursos,
#     asignaciones y asistencias generales.
#   - Docente: lectura de alumnos filtrada a sus propios cursos, y alta de
#     alumnos solo en cursos que imparte.
#   - Tutor: solo lectura (GET), filtrada a sus propios hijos.
admin_required = roles_required(ROLE_ADMIN)
staff_required = roles_required(ROLE_ADMIN, ROLE_DOCENTE)
authenticated_required = roles_required(ROLE_ADMIN, ROLE_DOCENTE, ROLE_TUTOR)
