"""Validación de payloads para la entidad `StudentCourses` (inscripción alumno-curso)."""
from marshmallow import Schema, fields, validate


class StudentCourseSchema(Schema):
    student_id = fields.Integer(required=True, validate=validate.Range(min=1))
    course_id = fields.Integer(required=True, validate=validate.Range(min=1))
