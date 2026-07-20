from sqlalchemy.orm import Session
from app.repositories.parentsrepository import ParentRepository
from app.models.parents import Parents

class ParentService:
    def __init__(self, db: Session):
        self.repository = ParentRepository(db)

    def register_parent(self, parent_data: dict) -> Parents:
        existing = self.repository.get_parent_by_name(parent_data.get("name"))
        if existing:
            raise ValueError("Ya existe un padre registrado con ese nombre.")
        return self.repository.registerParents(parent_data)

    def get_parent_by_name(self, parent_name: str) -> Parents:
        parent = self.repository.get_parent_by_name(parent_name)
        if not parent:
            raise ValueError(f"El tutor/padre '{parent_name}' no fue encontrado.")
        return parent

    def update_parent(self, parent_name: str, new_data: dict) -> bool:
        updated = self.repository.update_parent(parent_name, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: El tutor/padre '{parent_name}' no existe.")
        return True

    def delete_parent(self, parent_name: str) -> bool:
        deleted = self.repository.delete_parent(parent_name)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: El tutor/padre '{parent_name}' no existe.")
        return True