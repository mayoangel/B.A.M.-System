"""Validadores de Marshmallow reutilizables entre esquemas.

Centralizar estas reglas evita que cada esquema reinvente sus propios
umbrales de longitud/formato y mantiene consistencia con las restricciones
reales de las columnas definidas en `app/models/`.
"""
from marshmallow import validate

# Teléfono: 7 a 20 caracteres, dígitos y separadores comunes (+, -, espacios, paréntesis).
PHONE_REGEX = r"^[0-9+()\-\s]{7,20}$"

name_validator = validate.Length(min=2, max=100, error="Debe tener entre 2 y 100 caracteres.")
short_text_validator = validate.Length(min=1, max=100, error="Debe tener entre 1 y 100 caracteres.")
phone_validator = validate.Regexp(
    PHONE_REGEX,
    error="Teléfono inválido: usa entre 7 y 20 caracteres (dígitos, espacios, +, - o paréntesis).",
)
password_validator = validate.Length(
    min=8, max=128, error="La contraseña debe tener entre 8 y 128 caracteres."
)

STATUS_ACTIVO_INACTIVO = validate.OneOf(
    ["Activo", "Inactivo"], error="El estatus debe ser 'Activo' o 'Inactivo'."
)
