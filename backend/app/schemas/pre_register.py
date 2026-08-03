"""Validación de payloads para la entidad `PreRegister` (app/models/pre_register.py)."""
from marshmallow import Schema, fields, validate

from app.schemas.common import name_validator, phone_validator


class PreRegisterSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=name_validator)
    lastname = fields.String(required=True, validate=name_validator)
    surename = fields.String(required=False, allow_none=True, validate=validate.Length(max=100))
    email = fields.Email(required=True, validate=validate.Length(max=150))
    phone = fields.String(required=True, validate=phone_validator)
    course_id = fields.Integer(required=True, validate=validate.Range(min=1))
