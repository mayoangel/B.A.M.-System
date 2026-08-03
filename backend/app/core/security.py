
######### LO AGREGUE PARA EL REQUIRIEMIENTO 5   ##########

import bcrypt
from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings

# Cliente de cifrado simétrico reutilizado para los vectores biométricos
# (RF-02/RF-03). Se crea una sola vez por proceso.
_fernet = Fernet(settings.BIOMETRIC_ENCRYPTION_KEY)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        salt
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


######### Cifrado de datos biométricos (LFPDPPP) ##########
#
# Los vectores faciales NUNCA deben persistirse en texto plano. Se cifran
# de forma simétrica (Fernet/AES128-CBC + HMAC) con una llave del servidor
# (BIOMETRIC_ENCRYPTION_KEY) para poder desencriptarlos en memoria durante
# la comparación 1:N de RF-03.


def encrypt_vector(raw_vector: bytes) -> bytes:
    """Cifra los bytes crudos de un vector facial antes de guardarlos en BD."""
    return _fernet.encrypt(raw_vector)


def decrypt_vector(encrypted_vector: bytes) -> bytes:
    """Descifra un vector facial previamente cifrado con `encrypt_vector`."""
    try:
        return _fernet.decrypt(encrypted_vector)
    except InvalidToken as exc:
        raise ValueError(
            "No se pudo desencriptar el vector biométrico: token inválido o llave incorrecta."
        ) from exc