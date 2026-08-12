import os
import base64
import hashlib
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Settings:
    PROJECT_NAME: str = "BAM System"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root@localhost:3306/BAM_System?charset=utf8mb4"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "BAM_SECRET_2026"
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # Orígenes permitidos para CORS (frontend de React en desarrollo con Vite).
    # Configurable vía .env como lista separada por comas para producción.
    # Incluye el origen de Vercel en producción, p. ej.:
    # CORS_ORIGINS=http://localhost:5173,https://tu-app.vercel.app
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ]

    # Llave simétrica (Fernet) usada para cifrar los vectores faciales
    # (RF-02/RF-03) antes de guardarlos en la base de datos, según lo exige
    # la LFPDPPP para datos biométricos. DEBE definirse en el .env para
    # producción; el fallback solo existe para no romper el entorno local
    # y es determinístico para que los datos ya cifrados sigan siendo
    # legibles entre reinicios del mismo entorno.
    _env_key = os.getenv("BIOMETRIC_ENCRYPTION_KEY")
    if _env_key:
        BIOMETRIC_ENCRYPTION_KEY: bytes = _env_key.encode("utf-8")
    else:
        _dev_seed = hashlib.sha256(f"BAM-DEV-FALLBACK-{JWT_SECRET_KEY}".encode("utf-8")).digest()
        BIOMETRIC_ENCRYPTION_KEY: bytes = base64.urlsafe_b64encode(_dev_seed)

settings = Settings()