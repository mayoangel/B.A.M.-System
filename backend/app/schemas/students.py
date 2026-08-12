"""Validación de payloads para la entidad `Students` (app/models/students.py).

Los alumnos son menores de edad: no tienen credenciales ni datos de
contacto/dirección propios (eso vive en su tutor, ver `parents.py`), y su
matrícula (`id_student`) siempre la genera el backend
(`StudentService._generate_matricula`), nunca el cliente.
"""
from datetime import date

from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate, validates

from app.schemas.common import STATUS_ACTIVO_INACTIVO, name_validator

MIN_STUDENT_AGE = 3
MAX_STUDENT_AGE = 17  # Los alumnos deben ser menores de edad.


class StudentSchema(Schema):
    class Meta:
        # `id_student` es dump_only (generado por el servidor) y por lo tanto
        # no cuenta como campo "cargable"; sin este Meta, marshmallow lo
        # trataría como "Unknown field" si el cliente lo envía. `EXCLUDE`
        # permite que el payload lo incluya (será ignorado) en vez de fallar,
        # cumpliendo "ignorar cualquier matrícula que venga en el payload".
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    # Generada por el servidor: se documenta como dump_only para que la API
    # refleje que el cliente nunca debe (ni puede) fijarla.
    id_student = fields.String(dump_only=True)
    name = fields.String(required=True, validate=name_validator)
    lastname = fields.String(required=True, validate=name_validator)
    surename = fields.String(required=False, allow_none=True, validate=validate.Length(max=100))
    date_of_birth = fields.Date(required=True)
    status = fields.String(required=False, validate=STATUS_ACTIVO_INACTIVO)
    id_parent = fields.Integer(required=True, validate=validate.Range(min=1))
    created_at = fields.DateTime(dump_only=True)

    @validates("date_of_birth")
    def validate_is_minor(self, value, **kwargs):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if value > today:
            raise ValidationError("La fecha de nacimiento no puede estar en el futuro.")
        if age < MIN_STUDENT_AGE or age > MAX_STUDENT_AGE:
            raise ValidationError(
                "La fecha de nacimiento debe corresponder a un alumno menor de edad "
                f"(entre {MIN_STUDENT_AGE} y {MAX_STUDENT_AGE} años)."
            )
