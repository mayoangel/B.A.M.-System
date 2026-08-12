"""Excepciones de dominio del subsistema de reconocimiento facial.

Cubren el Enrolamiento (RF-02) y la Toma de Asistencia Automatizada (RF-03).
Viven en `services/` porque son parte de las reglas de negocio del dominio
biométrico (CLAUDE.md: "services/ ... la integración con el hardware o
biometría"), no de la capa de datos ni de la capa HTTP.
"""


class BiometricError(Exception):
    """Excepción base para cualquier error del motor de reconocimiento facial."""


class FaceNotDetectedError(BiometricError):
    """No se detectó ningún rostro en la imagen recibida ('Rostro no detectado')."""


class MultipleFacesDetectedError(BiometricError):
    """Se detectó más de un rostro cuando se esperaba exactamente uno."""


class PoorImageQualityError(BiometricError):
    """La imagen no cumple los mínimos de iluminación, nitidez o encuadre
    ('Mala iluminación', 'Imagen borrosa', 'Rostro muy lejano')."""


class AlreadyEnrolledError(BiometricError):
    """El usuario ya cuenta con información biométrica registrada."""


class DuplicateFaceError(BiometricError):
    """El rostro capturado ya está enrolado para otro usuario ('Rostro duplicado')."""


class NoEnrolledFacesError(BiometricError):
    """No existe ningún rostro enrolado contra el cual comparar."""


class FaceNotRecognizedError(BiometricError):
    """El rostro capturado no coincide con ningún usuario enrolado."""
