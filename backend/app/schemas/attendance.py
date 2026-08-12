"""Validación de payloads para la entidad `Attendance` (app/models/attendance.py)."""
from marshmallow import Schema, fields, validate


class AttendanceSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=False)   # si falta, el service usa la fecha de hoy
    time = fields.Time(required=False)   # si falta, el service usa la hora actual
    status = fields.String(required=True, validate=validate.Length(min=1, max=50))
    method = fields.String(required=True, validate=validate.Length(min=1, max=50))
    student_id = fields.Integer(required=True, validate=validate.Range(min=1))
    employee_id = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1))
    course_id = fields.Integer(required=True, validate=validate.Range(min=1))
