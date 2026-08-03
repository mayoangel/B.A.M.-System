from sqlalchemy.orm import Session
from app.repositories.parents_repository import ParentRepository
from app.models.parents import Parents
from app.core.security import hash_password

class ParentService:
    def __init__(self, db: Session):
        self.repository = ParentRepository(db)

    def register_parent(self, parent_data: dict) -> Parents:
        if not parent_data.get("email"):
            raise ValueError("El correo electrónico del tutor es obligatorio.")
        if not parent_data.get("password"):
            raise ValueError("La contraseña es obligatoria.")

        # Un mismo tutor puede registrar a varios hijos/as: si ya existe un
        # tutor con este correo, se reutiliza su registro en vez de fallar
        # por duplicado (el correo es UNIQUE en la base de datos).
        existing = self.repository.get_parent_by_email(parent_data.get("email"))
        if existing:
            return existing

        parent_data = dict(parent_data)
        parent_data["password"] = hash_password(parent_data["password"])

        return self.repository.registerParents(parent_data)

    def get_parent_by_name(self, parent_name: str) -> Parents:
        parent = self.repository.get_parent_by_name(parent_name)
        if not parent:
            raise ValueError(f"El tutor/padre '{parent_name}' no fue encontrado.")
        return parent

    def get_parent_by_id(self, parent_id: int, actor: dict | None = None) -> Parents:
        parent = self.repository.get_parent_by_id(parent_id)
        if not parent:
            raise ValueError(f"No se encontró al tutor con ID {parent_id}.")

        # RBAC: un tutor solo puede consultar su propio expediente.
        if actor and actor.get("role") == "tutor" and actor.get("id") != parent_id:
            raise PermissionError("Solo puedes consultar tu propia información de tutor.")

        return parent

    def update_parent(self, parent_name: str, new_data: dict) -> bool:
        new_data = self._hash_password_if_present(new_data)
        updated = self.repository.update_parent(parent_name, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: El tutor/padre '{parent_name}' no existe.")
        return True

    def update_parent_by_id(self, parent_id: int, new_data: dict) -> bool:
        new_data = self._hash_password_if_present(new_data)
        updated = self.repository.update_parent_by_id(parent_id, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: no existe un tutor con ID {parent_id}.")
        return True

    def delete_parent(self, parent_name: str) -> bool:
        deleted = self.repository.delete_parent(parent_name)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: El tutor/padre '{parent_name}' no existe.")
        return True

    @staticmethod
    def _hash_password_if_present(new_data: dict) -> dict:
        # Nunca se guarda una contraseña en texto plano (LFPDPPP): si el
        # payload de actualización trae una nueva contraseña, se hashea antes
        # de llegar al repositorio.
        new_data = dict(new_data)
        if new_data.get("password"):
            new_data["password"] = hash_password(new_data["password"])
        else:
            new_data.pop("password", None)
        return new_data
