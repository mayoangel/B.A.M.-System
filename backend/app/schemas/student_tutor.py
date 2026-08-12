"""Validación de payloads para la entidad `StudentTutor` (asignación tutor-alumno)."""
from marshmallow import Schema, fields, validate

from app.schemas.common import STATUS_ACTIVO_INACTIVO


class StudentTutorSchema(Schema):
    id = fields.Integer(dump_only=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    status = fields.String(required=False, validate=STATUS_ACTIVO_INACTIVO)
    student_id = fields.Integer(required=True, validate=validate.Range(min=1))
    employee_id = fields.Integer(required=True, validate=validate.Range(min=1))
