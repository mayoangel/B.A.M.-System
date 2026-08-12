"""Validación de payloads para la entidad `EmployeeCourse` (asignación profesor-curso)."""
from marshmallow import Schema, fields, validate


class EmployeeCourseSchema(Schema):
    employee_id = fields.Integer(required=True, validate=validate.Range(min=1))
    course_id = fields.Integer(required=True, validate=validate.Range(min=1))
