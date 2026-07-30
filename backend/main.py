from flask import Flask, g
from app.core.database import SessionLocal
from flask_jwt_extended import JWTManager

from app.api.v1.endpoints.parents import parents_bp
from app.api.v1.endpoints.pre_register import pre_register_bp
from app.api.v1.endpoints.reports import reports_bp
from app.api.v1.endpoints.roles import roles_bp
from app.api.v1.endpoints.student_course import enrollments_bp
from app.api.v1.endpoints.student_tutor import student_tutor_bp
from app.api.v1.endpoints.students import students_bp
from app.api.v1.endpoints.attendance import attendance_bp
from app.api.v1.endpoints.biometric_information import biometric_bp
from app.api.v1.endpoints.courses import courses_bp
from app.api.v1.endpoints.employees import employees_bp
from app.api.v1.endpoints.employee_course import employee_course_bp
from app.api.v1.endpoints.non_working_days import non_working_days_bp
from app.api.v1.endpoints.auth import auth_bp
from app.core.database import SessionLocal
from app.core.config import settings

app = Flask(__name__)


app.register_blueprint(students_bp, url_prefix="/api/v1/students")
app.register_blueprint(parents_bp, url_prefix="/api/v1/parents")
app.register_blueprint(pre_register_bp, url_prefix="/api/v1/pre-register")
app.register_blueprint(reports_bp, url_prefix="/api/v1/reports")
app.register_blueprint(roles_bp, url_prefix="/api/v1/roles")
app.register_blueprint(enrollments_bp, url_prefix="/api/v1/enrollments")
app.register_blueprint(student_tutor_bp, url_prefix="/api/v1/tutor-assignments")
app.register_blueprint(attendance_bp, url_prefix="/api/v1/attendance" )
app.register_blueprint(biometric_bp, url_prefix="/api/v1/biometrics")
app.register_blueprint(courses_bp, url_prefix="/api/v1/courses")
app.register_blueprint(employees_bp, url_prefix="/api/v1/employees")
app.register_blueprint(employee_course_bp, url_prefix="/api/v1/employee_course")
app.register_blueprint(non_working_days_bp, url_prefix="/api/v1/calendar")
app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

jwt = JWTManager(app)

@app.before_request
def before_request():
    g.db = SessionLocal()

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)