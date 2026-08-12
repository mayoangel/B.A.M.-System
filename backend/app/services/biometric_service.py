"""Servicio de dominio para el motor de reconocimiento facial.

Implementa:
  - RF-02 (Enrolamiento): `enroll_user`
  - RF-03 (Toma de Asistencia Automatizada): `identify_user`

Reglas de arquitectura (CLAUDE.md):
  - Esta capa NUNCA ejecuta SQL directamente; toda persistencia pasa por
    `BiometricRepository`.
  - El vector facial se cifra (LFPDPPP) antes de tocar el repositorio; jamás
    se guarda en texto plano.
  - El stack de IA (OpenCV/InsightFace/ONNX Runtime) vive exclusivamente en
    `face_engine.py`; este archivo solo orquesta reglas de negocio.
"""
from __future__ import annotations

import hashlib
import logging
import threading
import time
from datetime import datetime

import numpy as np
from sqlalchemy.orm import Session

from app.core.security import encrypt_vector, decrypt_vector
from app.models.biometric_information import BiometricInformation
from app.repositories.biometric_repository import BiometricRepository
from app.services.biometric_exceptions import (
    AlreadyEnrolledError,
    DuplicateFaceError,
    FaceNotRecognizedError,
    NoEnrolledFacesError,
)
from app.services.face_engine import FaceEngine

logger = logging.getLogger(__name__)


class BiometricService:
    # Umbral de similitud coseno para considerar dos vectores como la misma
    # persona. ArcFace/InsightFace (buffalo_l) separa bien identidades
    # distintas por encima de ~0.45-0.5 con esta métrica.
    RECOGNITION_THRESHOLD = 0.45

    # Objetivo de rendimiento de RF-03 (idealmente 0.5-1.5s, tope 3s).
    MAX_PROCESSING_SECONDS = 3.0

    # --- Estado compartido a nivel de proceso -------------------------------
    # El modelo de IA y la caché de vectores desencriptados se comparten
    # entre todas las instancias de BiometricService del mismo worker para
    # no recargar el modelo ni desencriptar en cada request.
    _face_engine: FaceEngine | None = None
    _engine_lock = threading.Lock()
    _cache_lock = threading.Lock()
    _vector_cache: dict[int, np.ndarray] = {}
    _cache_loaded: bool = False

    def __init__(self, db: Session):
        self.repository = BiometricRepository(db)
        self._ensure_engine_loaded()

    @classmethod
    def _ensure_engine_loaded(cls) -> None:
        if cls._face_engine is None:
            with cls._engine_lock:
                if cls._face_engine is None:
                    cls._face_engine = FaceEngine()

    @property
    def engine(self) -> FaceEngine:
        return BiometricService._face_engine

    # -------------------------------------------------------------------
    # RF-02: Enrolamiento
    # -------------------------------------------------------------------
    def enroll_user(self, image_bytes: bytes, user_id: int) -> BiometricInformation:
        """Enrola el rostro de un alumno/empleado a partir de una foto.

        Flujo: valida -> extrae vector -> valida duplicados -> cifra -> persiste.
        """
        if not user_id:
            raise ValueError("El ID del usuario es obligatorio.")

        existing = self.repository.getBiometricByStudentId(user_id)
        if existing:
            raise AlreadyEnrolledError(
                f"El usuario con ID {user_id} ya cuenta con información biométrica registrada."
            )

        embedding = self.engine.extract_embedding(image_bytes, expect_single_face=True)

        self._ensure_cache_loaded()
        duplicate_id = self._find_duplicate(embedding)
        if duplicate_id is not None:
            raise DuplicateFaceError(
                "Rostro duplicado: este rostro ya está enrolado para el usuario "
                f"con ID {duplicate_id}. No es posible enrolar el mismo rostro dos veces."
            )

        raw_vector = embedding.tobytes()
        encrypted_vector = encrypt_vector(raw_vector)

        biometric_data = {
            "student_id": user_id,
            "face_vector": encrypted_vector.decode("utf-8"),
            "encryption_hash": hashlib.sha256(encrypted_vector).hexdigest(),
            "enrollment_date": datetime.now(),
        }

        record = self.repository.registerBiometric(biometric_data)

        with BiometricService._cache_lock:
            BiometricService._vector_cache[user_id] = embedding

        logger.info("Enrolamiento biométrico completado para el usuario %s.", user_id)
        return record

    # -------------------------------------------------------------------
    # RF-03: Toma de asistencia automatizada
    # -------------------------------------------------------------------
    def identify_user(self, image_bytes: bytes) -> dict:
        """Identifica a la persona frente a la cámara comparando contra la
        caché de vectores enrolados. Objetivo: < 3s (ideal 0.5-1.5s).
        """
        start = time.perf_counter()

        self._ensure_cache_loaded()
        if not BiometricService._vector_cache:
            raise NoEnrolledFacesError(
                "No hay ningún usuario enrolado en el sistema biométrico todavía."
            )

        probe_embedding = self.engine.extract_embedding(image_bytes, expect_single_face=True)

        best_user_id, best_score = self._find_best_match(probe_embedding)

        elapsed = time.perf_counter() - start
        if elapsed > self.MAX_PROCESSING_SECONDS:
            logger.warning(
                "identify_user superó el objetivo de rendimiento: %.3fs (límite %.1fs).",
                elapsed, self.MAX_PROCESSING_SECONDS
            )
        else:
            logger.info("identify_user resuelto en %.3fs (score=%.4f).", elapsed, best_score)

        if best_user_id is None or best_score < self.RECOGNITION_THRESHOLD:
            raise FaceNotRecognizedError(
                "Rostro no reconocido: no coincide con ningún usuario enrolado."
            )

        return {
            "student_id": best_user_id,
            "confidence": round(float(best_score), 4),
            "processing_time_seconds": round(elapsed, 3),
        }

    def refresh_cache(self) -> int:
        """Fuerza una recarga completa de la caché desde la base de datos.

        Útil tras operaciones masivas o si se sospecha que la caché quedó
        desincronizada respecto a la BD. Devuelve el número de vectores cargados.
        """
        self._ensure_cache_loaded(force_refresh=True)
        return len(BiometricService._vector_cache)

    # -------------------------------------------------------------------
    # Administración (mantenido por compatibilidad / uso manual - RF-08)
    # -------------------------------------------------------------------
    def register_biometric(self, biometric_data: dict) -> BiometricInformation:
        """Alta manual de un vector ya calculado externamente (uso administrativo).

        Se mantiene por compatibilidad; el flujo recomendado para RF-02 es
        `enroll_user`, que calcula y cifra el vector a partir de una imagen.
        """
        if not biometric_data.get("student_id"):
            raise ValueError("El ID del estudiante es obligatorio.")
        if not biometric_data.get("face_vector"):
            raise ValueError("El vector facial es obligatorio para el reconocimiento biométrico.")
        if not biometric_data.get("encryption_hash"):
            raise ValueError("El hash de encriptación de seguridad es obligatorio.")

        if not biometric_data.get("enrollment_date"):
            biometric_data["enrollment_date"] = datetime.now()

        existing = self.repository.getBiometricByStudentId(biometric_data.get("student_id"))
        if existing:
            raise AlreadyEnrolledError("El estudiante ya cuenta con información biométrica registrada.")

        return self.repository.registerBiometric(biometric_data)

    def get_biometric_by_student_id(self, student_id: int) -> BiometricInformation:
        biometric = self.repository.getBiometricByStudentId(student_id)
        if not biometric:
            raise ValueError(f"No se encontró información biométrica para el estudiante con ID {student_id}")
        return biometric

    def delete_biometric(self, student_id: int) -> bool:
        deleted = self.repository.deleteBiometric(student_id)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: No existe información biométrica para el estudiante {student_id}")

        with BiometricService._cache_lock:
            BiometricService._vector_cache.pop(student_id, None)
        return True

    # -------------------------------------------------------------------
    # Helpers internos de caché / comparación
    # -------------------------------------------------------------------
    def _ensure_cache_loaded(self, force_refresh: bool = False) -> None:
        if BiometricService._cache_loaded and not force_refresh:
            return

        with BiometricService._cache_lock:
            if BiometricService._cache_loaded and not force_refresh:
                return
            BiometricService._vector_cache = self._load_all_vectors()
            BiometricService._cache_loaded = True

    def _load_all_vectors(self) -> dict[int, np.ndarray]:
        records = self.repository.getAllBiometrics()
        cache: dict[int, np.ndarray] = {}
        for record in records:
            try:
                raw = decrypt_vector(record.face_vector.encode("utf-8"))
                cache[record.student_id] = np.frombuffer(raw, dtype=np.float32).copy()
            except Exception:
                logger.exception(
                    "No se pudo desencriptar el vector biométrico del usuario %s; se omite de la caché.",
                    record.student_id,
                )
        return cache

    def _find_duplicate(self, embedding: np.ndarray) -> int | None:
        best_id, best_score = self._find_best_match(embedding)
        if best_id is not None and best_score >= self.RECOGNITION_THRESHOLD:
            return best_id
        return None

    @classmethod
    def _find_best_match(cls, embedding: np.ndarray) -> tuple[int | None, float]:
        best_id: int | None = None
        best_score = -1.0
        for user_id, stored_embedding in cls._vector_cache.items():
            score = cls._cosine_similarity(embedding, stored_embedding)
            if score > best_score:
                best_score = score
                best_id = user_id
        return best_id, best_score

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        denom = float(np.linalg.norm(a) * np.linalg.norm(b))
        if denom == 0.0:
            return 0.0
        return float(np.dot(a, b) / denom)
