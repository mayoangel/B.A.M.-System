"""Validación de payloads para la entidad `Courses` (app/models/courses.py)."""
from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from app.schemas.common import STATUS_ACTIVO_INACTIVO, short_text_validator


class CourseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    description = fields.String(required=True, validate=validate.Length(min=1, max=100))
    category = fields.String(required=True, validate=short_text_validator)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    time_duration = fields.String(required=True, validate=validate.Length(min=1, max=50))
    days_of_week = fields.String(required=True, validate=validate.Length(min=1, max=50))
    status = fields.String(required=False, validate=STATUS_ACTIVO_INACTIVO)

    @validates_schema
    def validate_date_range(self, data, **kwargs):
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and start >= end:
            raise ValidationError(
                "'end_date' debe ser posterior a 'start_date'.", field_name="end_date"
            )
