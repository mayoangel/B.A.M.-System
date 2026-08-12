"""Validación de payloads para la entidad `Employees` (app/models/employees.py)."""
from marshmallow import Schema, fields, validate

from app.schemas.common import (
    STATUS_ACTIVO_INACTIVO,
    name_validator,
    password_validator,
    phone_validator,
)


class EmployeeSchema(Schema):
    id = fields.Integer(dump_only=True)
    id_employee = fields.String(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=name_validator)
    lastname = fields.String(required=True, validate=name_validator)
    surename = fields.String(required=False, allow_none=True, validate=validate.Length(max=100))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    password = fields.String(required=True, load_only=True, validate=password_validator)
    phone = fields.String(required=True, validate=phone_validator)
    age = fields.Integer(required=True, validate=validate.Range(min=18, max=100))
    status = fields.String(required=False, validate=STATUS_ACTIVO_INACTIVO)
    dir_street = fields.String(required=True, validate=validate.Length(min=1, max=100))
    dir_col = fields.String(required=True, validate=validate.Length(min=1, max=100))
    dir_num = fields.String(required=True, validate=validate.Length(min=1, max=100))
    role_id = fields.Integer(required=True, validate=validate.Range(min=1))
