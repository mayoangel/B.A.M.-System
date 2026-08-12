"""Motor de reconocimiento facial (RF-02 / RF-03).

Esta es la ÚNICA pieza del sistema que conoce el stack de IA
(OpenCV + InsightFace + ONNX Runtime). El resto de la capa de servicios
(`biometric_service.py`) solo conoce la interfaz pública de `FaceEngine`
y las excepciones de `biometric_exceptions.py`.

Cámara de referencia: Logitech C920 (idealmente 1920x1080, imagen nítida).
Los umbrales de calidad de abajo están calibrados para ese escenario, pero el
umbral de nitidez se escala según la resolución real de cada frame para
seguir funcionando con cámaras de menor calidad (ver `SHARPNESS_REFERENCE_AREA`).
"""
from __future__ import annotations

import logging
import threading

import cv2
import numpy as np

from app.services.biometric_exceptions import (
    FaceNotDetectedError,
    MultipleFacesDetectedError,
    PoorImageQualityError,
)

logger = logging.getLogger(__name__)

# --- Modelo InsightFace -----------------------------------------------------
MODEL_NAME = "buffalo_l"          # paquete de modelos de detección + ArcFace de InsightFace
EMBEDDING_DIM = 512               # dimensión del vector facial que produce buffalo_l
DEFAULT_DET_SIZE = (640, 640)     # tamaño de entrada del detector (RetinaFace)

# --- Umbrales de calidad de imagen ------------------------------------------
MIN_DETECTION_SCORE = 0.55        # confianza mínima del detector de rostros
MIN_FACE_AREA_RATIO = 0.02        # el rostro debe ocupar al menos ~2% del frame (ratio, no depende de la resolución)
MIN_BRIGHTNESS = 60.0             # brillo medio en escala de grises (0-255)
MAX_BRIGHTNESS = 200.0

# La varianza del Laplaciano (nitidez) depende de cuántos píxeles tiene la
# imagen: una cámara de menor resolución (ej. webcams USB genéricas VGA)
# produce valores más bajos que una Logitech C920 en 1920x1080 aunque el
# encuadre esté igualmente enfocado. Por eso el umbral se calibra para una
# resolución de referencia y se escala proporcionalmente al área real de
# cada frame, con un piso absoluto para seguir rechazando imágenes
# genuinamente borrosas sin importar la cámara.
MIN_SHARPNESS = 80.0
SHARPNESS_REFERENCE_AREA = 1920 * 1080
MIN_SHARPNESS_FLOOR = 15.0


class FaceEngine:
    """Wrapper perezoso y thread-safe sobre `insightface.app.FaceAnalysis`.

    La carga del modelo ONNX es costosa (lectura de disco + inicialización de
    ONNX Runtime), por lo que se hace una sola vez por proceso, la primera
    vez que se necesita, y se reutiliza para todas las requests siguientes.
    """

    def __init__(self, providers: list[str] | None = None, det_size: tuple[int, int] = DEFAULT_DET_SIZE):
        self._providers = providers or ["CPUExecutionProvider"]
        self._det_size = det_size
        self._app = None
        self._load_lock = threading.Lock()

    def _get_app(self):
        if self._app is not None:
            return self._app

        with self._load_lock:
            if self._app is None:
                # Import perezoso: insightface/onnxruntime son dependencias
                # pesadas y no deben cargarse si el servicio nunca se usa.
                from insightface.app import FaceAnalysis

                logger.info("Cargando modelo InsightFace '%s' (providers=%s)...", MODEL_NAME, self._providers)
                face_app = FaceAnalysis(name=MODEL_NAME, providers=self._providers)
                face_app.prepare(ctx_id=0, det_size=self._det_size)
                self._app = face_app
                logger.info("Modelo InsightFace '%s' listo.", MODEL_NAME)

        return self._app

    def extract_embedding(self, image_bytes: bytes, expect_single_face: bool = True) -> np.ndarray:
        """Decodifica la imagen, valida su calidad y devuelve el vector facial (512,).

        Lanza `FaceNotDetectedError`, `MultipleFacesDetectedError` o
        `PoorImageQualityError` según corresponda.
        """
        image = self._decode_image(image_bytes)
        logger.info("Imagen recibida: %dx%d px.", image.shape[1], image.shape[0])
        self._validate_frame_quality(image)

        faces = self._get_app().get(image)

        if not faces:
            raise FaceNotDetectedError(
                "Rostro no detectado: verifica el encuadre, la distancia a la cámara y vuelve a intentar."
            )

        if expect_single_face and len(faces) > 1:
            raise MultipleFacesDetectedError(
                f"Se detectaron {len(faces)} rostros en la imagen; debe haber una sola persona frente a la cámara."
            )

        face = max(faces, key=lambda f: f.det_score)
        logger.info("Confianza de detección (det_score) = %.4f (mínimo %.2f).", float(face.det_score), MIN_DETECTION_SCORE)

        if float(face.det_score) < MIN_DETECTION_SCORE:
            raise PoorImageQualityError(
                "Mala iluminación o encuadre: la confianza de detección del rostro es demasiado baja."
            )

        self._validate_face_size(face, image.shape)

        embedding = np.asarray(face.normed_embedding, dtype=np.float32)
        return embedding

    @staticmethod
    def _decode_image(image_bytes: bytes) -> np.ndarray:
        if not image_bytes:
            raise ValueError("No se recibieron datos de imagen.")

        buffer = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("No se pudo decodificar la imagen: formato no soportado o archivo corrupto.")

        return image

    @staticmethod
    def _validate_frame_quality(image: np.ndarray) -> None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        brightness = float(np.mean(gray))
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        frame_area = float(gray.shape[0] * gray.shape[1])
        scaled_min_sharpness = max(
            MIN_SHARPNESS_FLOOR, MIN_SHARPNESS * (frame_area / SHARPNESS_REFERENCE_AREA)
        )

        logger.info(
            "Calidad de imagen: brillo=%.1f (rango %.0f-%.0f), nitidez=%.1f (mínimo %.1f para %dx%d px).",
            brightness, MIN_BRIGHTNESS, MAX_BRIGHTNESS, sharpness, scaled_min_sharpness,
            gray.shape[1], gray.shape[0],
        )

        if brightness < MIN_BRIGHTNESS:
            raise PoorImageQualityError("Mala iluminación: la imagen está demasiado oscura.")
        if brightness > MAX_BRIGHTNESS:
            raise PoorImageQualityError("Mala iluminación: la imagen está sobreexpuesta.")

        if sharpness < scaled_min_sharpness:
            raise PoorImageQualityError(
                "Imagen borrosa: mantén la cámara y el rostro estables durante la captura."
            )

    @staticmethod
    def _validate_face_size(face, image_shape: tuple[int, int, int]) -> None:
        x1, y1, x2, y2 = face.bbox
        face_area = max(0.0, float(x2 - x1)) * max(0.0, float(y2 - y1))
        frame_area = float(image_shape[0] * image_shape[1])
        ratio = (face_area / frame_area) if frame_area > 0 else 0.0
        logger.info("Tamaño de rostro: %.4f del frame (mínimo %.4f).", ratio, MIN_FACE_AREA_RATIO)

        if frame_area <= 0 or ratio < MIN_FACE_AREA_RATIO:
            raise PoorImageQualityError(
                "El rostro está demasiado lejos de la cámara; acércate e inténtalo de nuevo."
            )
