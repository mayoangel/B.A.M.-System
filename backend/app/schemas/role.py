"""Validación de payloads para la entidad `Role` (app/models/role.py)."""
from marshmallow import Schema, fields, validate


class RoleSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    description = fields.String(required=True, validate=validate.Length(min=1, max=100))
