import re
from typing import List
from sqlalchemy.orm import Session
from app.repositories.pre_register_repository import PreRegisterRepository
from app.models.pre_register import PreRegister

class PreRegisterService:
    def __init__(self, db: Session):
        self.repository = PreRegisterRepository(db)

    def create_pre_register(self, pre_data: dict) -> PreRegister:
        if not pre_data.get("name") or not pre_data.get("lastname"):
            raise ValueError("El nombre y el apellido paterno son obligatorios.")
        if not pre_data.get("email") or not pre_data.get("phone"):
            raise ValueError("El correo electrónico y el teléfono son obligatorios.")
        if not pre_data.get("course_id"):
            raise ValueError("Debe especificar el ID del curso al que desea pre-registrarse.")

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, pre_data.get("email")):
            raise ValueError("El formato del correo electrónico es inválido.")

        return self.repository.create_pre_register(pre_data)

    def get_pre_register_by_id(self, pre_id: int) -> PreRegister:
        pre_reg = self.repository.get_pre_register_by_id(pre_id)
        if not pre_reg:
            raise ValueError(f"No se encontró el pre-registro con ID {pre_id}")
        return pre_reg

    def get_pre_registers_by_course(self, course_id: int) -> List[PreRegister]:
        return self.repository.get_pre_registers_by_course(course_id)

    def get_all_pre_registers(self) -> List[PreRegister]:
        return self.repository.get_all_pre_registers()

    def delete_pre_register(self, pre_id: int) -> bool:
        deleted = self.repository.delete_pre_register(pre_id)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: El pre-registro con ID {pre_id} no existe.")
        return True