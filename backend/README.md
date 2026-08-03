# B.A.M. System — Backend

API en Flask con arquitectura limpia (`api/` → `services/` → `repositories/` → BD).

## Requisitos

- **Python 3.10, 3.11 o 3.12.** El motor de reconocimiento facial (`insightface`,
  que depende de `scikit-image`/`scikit-learn`) todavía no publica wheels
  precompilados para Python 3.13 en Windows; instalar con 3.13 provocará que
  `pip` intente compilar `scikit-learn` desde fuente y falle.
- MySQL (ver `/database/schema.sql`).

## Instalación

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## Variables de entorno (`.env`)

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | Cadena de conexión SQLAlchemy a MySQL. |
| `JWT_SECRET_KEY` | Llave de firma de los tokens JWT. |
| `BIOMETRIC_ENCRYPTION_KEY` | Llave Fernet (32 bytes urlsafe-base64) para cifrar los vectores faciales antes de guardarlos (LFPDPPP). **Obligatoria en producción** — sin ella se usa un fallback derivado de `JWT_SECRET_KEY` solo apto para desarrollo local. Generar una con: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` |

## Motor de reconocimiento facial (RF-02 / RF-03)

- La primera vez que se usa `BiometricService`, InsightFace descarga
  automáticamente el paquete de modelos `buffalo_l` (~300 MB) a
  `~/.insightface/models/`. Requiere conexión a internet la primera vez.
- Cámara de referencia: Logitech C920 a 1920x1080. Los umbrales de calidad
  de imagen (brillo, nitidez, tamaño del rostro) están calibrados para esa
  resolución; ver `app/services/face_engine.py`.
- Endpoints: `POST /api/v1/biometrics/enroll` (multipart: `image`, `user_id`)
  y `POST /api/v1/biometrics/identify` (multipart: `image`).
