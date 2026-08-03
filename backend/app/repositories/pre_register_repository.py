from sqlalchemy.orm import Session
from app.models.pre_register import PreRegister
class PreRegisterRepository:
    def __init__(self, db: Session):
        self.db = db

    # 1. Crear un nuevo pre-registro 
    def create_pre_register(self, pre_data: dict) -> PreRegister:
        db_pre = PreRegister(**pre_data)
        self.db.add(db_pre)
        self.db.commit()
        self.db.refresh(db_pre)
        return db_pre

    # 2. Buscar un pre-registro por ID 
    def get_pre_register_by_id(self, pre_id: int) -> PreRegister:
        return self.db.query(PreRegister).filter(PreRegister.id == pre_id).first()

    # 3. Obtener todos los pre-registros de un curso específico 
    def get_pre_registers_by_course(self, course_id: int):
        return self.db.query(PreRegister).filter(PreRegister.course_id == course_id).all()

    # 4. Obtener todos los pre-registros pendientes en el sistema
    def get_all_pre_registers(self):
        return self.db.query(PreRegister).order_by(PreRegister.created_at.desc()).all()

    # 5. Eliminar un pre-registro 
    def delete_pre_register(self, pre_id: int) -> bool:
        db_pre = self.get_pre_register_by_id(pre_id)
        if db_pre:
            self.db.delete(db_pre)
            self.db.commit()
            return True
        return False