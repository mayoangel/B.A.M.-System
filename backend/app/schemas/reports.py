"""Validación de payloads para la entidad `Reports` (app/models/reports.py)."""
from marshmallow import Schema, fields, validate


class ReportSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    generation_date = fields.DateTime(required=False)  # si falta, el service usa datetime.now()
    employee_id = fields.Integer(required=True, validate=validate.Range(min=1))
