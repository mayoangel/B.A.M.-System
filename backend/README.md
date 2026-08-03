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

## Autenticación y control de acceso por roles (RBAC)

`POST /api/v1/auth/login` es un login unificado: recibe `{ email, password }`
y busca la cuenta primero entre los **Empleados** (Administrador/Docente) y,
si no hay coincidencia, entre los **Tutores** (`parents`). El JWT resultante
incluye los claims `role` (`admin` | `docente` | `tutor`) y `actor_type`
(`employee` | `parent`), que son los que valida `app/core/permissions.py` en
cada endpoint protegido.

Reglas de acceso:

- **Administrador** (`role_id = 1` en `employees`): acceso total (CRUD) a
  alumnos, docentes, cursos, asignaciones y asistencias.
- **Docente** (cualquier otro `role_id`, ej. Profesor/Prefecto): solo lectura
  de alumnos, filtrada a los inscritos en los cursos que imparte; puede
  registrar alumnos (`POST /students/`) y enrolar su biometría, pero solo
  puede inscribirlos (`POST /enrollments/enroll`) en un curso propio, y solo
  puede tomar asistencia (`POST /attendance/`) para sus propios cursos.
- **Tutor** (tabla `parents`, con `email`/`password` propios): solo lectura
  (GET), filtrada siempre por su `parent_id` (extraído del JWT) — únicamente
  ve a sus propios hijos y la asistencia/cursos asociados.

Todas las peticiones protegidas requieren el header
`Authorization: Bearer <token>`.

### Credenciales de prueba (datos semilla)

La contraseña de **todas** las cuentas semilla (`database/seeds.sql`) es
`Bam2026!`:

| Rol | Correo |
|---|---|
| Administrador | `ana.gomez@bam.com` |
| Docente | `roberto.sanchez@bam.com` |
| Docente (Prefecto) | `lucia.torres@bam.com` |
| Tutor | `carlos.mendoza@mail.com` |
| Tutor | `gabriela.espinoza@mail.com` |
| Tutor | `manuel.castro@mail.com` |
