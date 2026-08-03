"""Validación de payloads para la entidad `NonWorkingDays` (app/models/non_working_days.py)."""
from marshmallow import Schema, fields, validate


class NonWorkingDaySchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    description = fields.String(required=True, validate=validate.Length(min=1, max=150))
