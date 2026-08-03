"""Agregador central de rutas de la API v1.

Este módulo es el único responsable de conocer todos los blueprints
definidos en `app/api/v1/endpoints/` y los prefijos con los que se
exponen. `main.py` solo debe importar `register_routes` desde aquí.
"""

from app.api.v1.endpoints.attendance import attendance_bp
from app.api.v1.endpoints.auth import auth_bp
from app.api.v1.endpoints.biometric_information import biometric_bp
from app.api.v1.endpoints.courses import courses_bp
from app.api.v1.endpoints.employee_course import employee_course_bp
from app.api.v1.endpoints.employees import employees_bp
from app.api.v1.endpoints.non_working_days import non_working_days_bp
from app.api.v1.endpoints.parents import parents_bp
from app.api.v1.endpoints.pre_register import pre_register_bp
from app.api.v1.endpoints.reports import reports_bp
from app.api.v1.endpoints.roles import roles_bp
from app.api.v1.endpoints.student_course import enrollments_bp
from app.api.v1.endpoints.student_tutor import student_tutor_bp
from app.api.v1.endpoints.students import students_bp

BLUEPRINTS = (
    (students_bp, "/api/v1/students"),
    (parents_bp, "/api/v1/parents"),
    (pre_register_bp, "/api/v1/pre-register"),
    (reports_bp, "/api/v1/reports"),
    (roles_bp, "/api/v1/roles"),
    (enrollments_bp, "/api/v1/enrollments"),
    (student_tutor_bp, "/api/v1/tutor-assignments"),
    (attendance_bp, "/api/v1/attendance"),
    (biometric_bp, "/api/v1/biometrics"),
    (courses_bp, "/api/v1/courses"),
    (employees_bp, "/api/v1/employees"),
    (employee_course_bp, "/api/v1/employee_course"),
    (non_working_days_bp, "/api/v1/calendar"),
    (auth_bp, "/api/v1/auth"),
)


def register_routes(app) -> None:
    """Registra todos los blueprints de la API v1 en la aplicación Flask."""
    for blueprint, url_prefix in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
