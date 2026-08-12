"""Validación de payloads para la entidad `Parents` (app/models/parents.py).

El tutor es ahora el único titular de credenciales, contacto y dirección en
la relación alumno-tutor (los alumnos son menores de edad y no tienen estos
datos propios).
"""
from marshmallow import Schema, fields, validate

from app.schemas.common import name_validator, password_validator, phone_validator


class ParentSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=name_validator)
    lastname = fields.String(required=True, validate=name_validator)
    surename = fields.String(required=False, allow_none=True, validate=validate.Length(max=100))
    phone = fields.String(required=True, validate=phone_validator)
    email = fields.Email(required=True, validate=validate.Length(max=150))
    password = fields.String(required=True, load_only=True, validate=password_validator)
    dir_street = fields.String(required=True, validate=validate.Length(min=1, max=150))
    dir_col = fields.String(required=True, validate=validate.Length(min=1, max=100))
    dir_num = fields.String(required=True, validate=validate.Length(min=1, max=50))
