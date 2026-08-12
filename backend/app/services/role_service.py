from sqlalchemy.orm import Session
from app.repositories.role_repository import RoleRepository

class RoleService:
    def __init__(self, db: Session):
        self.repo = RoleRepository(db)

    def create_role(self, role_data: dict):
        if not role_data.get("name"):
            raise ValueError("El campo de nombre es obligatorio")

        if not role_data.get("description"):
            raise ValueError("El campo de descripción es obligatorio")

        exist = self.repo.get_role_by_name(role_data.get("name"))
        if exist:
            raise ValueError(f"El rol '{role_data.get('name')}' ya existe.")

        return self.repo.registerRole(role_data)
    
    def list_all_roles(self) -> list:
        return self.repo.getAllRoles()
    
    def get_Role_Name(self, name: str):
        role = self.repo.get_role_by_name(name)
        if not role:
            raise ValueError(f"El rol '{name}' no existe.")
        return role

    def update_Role(self, name: str, new_data: dict):
        updated = self.repo.update_role(name, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: El rol '{name}' no existe.")
        return True

    def delete_Role(self, name: str):
        deleted = self.repo.delete_role(name)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: El rol '{name}' no existe.")
        return True