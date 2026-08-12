"""Esquemas de Marshmallow (DTOs de validación de entrada).

Cada esquema valida el payload JSON que llega a los endpoints en
`app/api/v1/endpoints/` ANTES de que los datos se envíen a `app/services/`.
Las definiciones de tablas (SQLAlchemy `Base`) viven en `app/models/`.
"""
from app.schemas.attendance import AttendanceSchema
from app.schemas.biometric_information import BiometricInformationSchema
from app.schemas.courses import CourseSchema
from app.schemas.employee_course import EmployeeCourseSchema
from app.schemas.employees import EmployeeSchema
from app.schemas.non_working_days import NonWorkingDaySchema
from app.schemas.parents import ParentSchema
from app.schemas.pre_register import PreRegisterSchema
from app.schemas.reports import ReportSchema
from app.schemas.role import RoleSchema
from app.schemas.student_courses import StudentCourseSchema
from app.schemas.student_tutor import StudentTutorSchema
from app.schemas.students import StudentSchema

__all__ = [
    "AttendanceSchema",
    "BiometricInformationSchema",
    "CourseSchema",
    "EmployeeCourseSchema",
    "EmployeeSchema",
    "NonWorkingDaySchema",
    "ParentSchema",
    "PreRegisterSchema",
    "ReportSchema",
    "RoleSchema",
    "StudentCourseSchema",
    "StudentTutorSchema",
    "StudentSchema",
]
