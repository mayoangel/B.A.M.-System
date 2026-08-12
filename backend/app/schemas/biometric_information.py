"""Validación de payloads para la entidad `BiometricInformation`.

Nota: solo aplica al alta manual/administrativa (`POST /biometrics/`, un
vector ya calculado externamente). Los endpoints `/enroll` y `/identify`
(RF-02/RF-03) reciben una imagen vía multipart, no JSON, y su validación de
calidad/rostro vive en `app/services/face_engine.py`.
"""
from marshmallow import Schema, fields, validate


class BiometricInformationSchema(Schema):
    id = fields.Integer(dump_only=True)
    student_id = fields.Integer(required=True, validate=validate.Range(min=1))
    face_vector = fields.String(required=True, validate=validate.Length(min=1))
    encryption_hash = fields.String(required=True, validate=validate.Length(min=1, max=255))
    enrollment_date = fields.DateTime(required=False)
