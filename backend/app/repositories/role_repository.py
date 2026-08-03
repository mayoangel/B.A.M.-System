from sqlalchemy.orm import Session
from app.models.role import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    #crear roles
    def registerRole(self, role_data: dict) -> Role:
        db_role = Role(**role_data)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role
    
    # Traer todos los roles registrados
    def getAllRoles(self) -> list[Role]:
        return self.db.query(Role).all()

    #buscar rol por nombre
    def get_role_by_name(self, roleName: str) -> Role:
        return self.db.query(Role).filter(Role.name == roleName).first()

    #actualizar roles
    def update_role(self, roleName: str, new_data: dict) -> bool:
        db_role = self.get_role_by_name(roleName)
        if db_role:
            for key, value in new_data.items():
                setattr(db_role, key, value)
            self.db.commit()
            return True
        return False

    #eliminar roles
    def delete_role(self, roleName: str) -> bool:
        db_role = self.get_role_by_name(roleName)
        if db_role:
            self.db.delete(db_role)
            self.db.commit()
            return True
        return False