from sqlalchemy.orm import Session
from app.models.parents import Parents

class ParentRepository:
    def __init__(self,db:Session):
        self.db = db

    #crear padres
    def registerParents(self, parent_data: dict) -> Parents:
        db_parent = Parents(**parent_data)
        self.db.add(db_parent)
        self.db.commit()
        self.db.refresh(db_parent)
        return db_parent

    #buscar padres
    def get_parent_by_name(self, parentName: str) -> Parents:
        return self.db.query(Parents).filter(Parents.name == parentName).first()

    # Buscar padres/tutores por ID
    def get_parent_by_id(self, parent_id: int) -> Parents:
        return self.db.query(Parents).filter(Parents.id == parent_id).first()

    #actualizar padres
    def update_parent(self, parentName: str, new_data: dict) -> bool:
        db_parent = self.get_parent_by_name(parentName)
        if db_parent:
            for key, value in new_data.items():
                setattr(db_parent, key, value)
            self.db.commit()
            return True
        return False

    #eliminar padres
    def delate_parent(self, parentName: str) -> bool:
        db_parent = self.get_parent_by_name(parentName)
        if db_parent:
            self.db.delete(db_parent)
            self.db.commit()
            return True
        return False