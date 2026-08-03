
######### LO AGREGUE PARA EL REQUIRIEMIENTO 5   ##########

from flask_jwt_extended import create_access_token
from app.repositories.employees_repository import EmployeeRepository
from app.core.security import verify_password


class AuthService:

    def __init__(self, db):
        self.repository = EmployeeRepository(db)

    def login(self, email, password):

        employee = self.repository.getEmployeeByEmail(email)

        if not employee:
            return None

        if not verify_password(
            password,
            employee.password
        ):
            return None

        token = create_access_token(
            identity=str(employee.id),
            additional_claims={
                "role_id": employee.role_id,
                "name": employee.name
            }
        )

        return {
            "token": token,
            "employee_id": employee.id,
            "name": employee.name,
            "role_id": employee.role_id
        }

    def get_profile(self, employee_id):
        employee = self.repository.getEmployeeById(employee_id)

        if not employee:
            return None

        return {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "role_id": employee.role_id
        }

    def change_role(self, requester_role_id, employee_id, new_role_id):
        if requester_role_id != 1:
            raise PermissionError("Solo administradores")

        if not employee_id or not new_role_id:
            raise ValueError("employee_id y role_id son obligatorios")

        updated = self.repository.updateEmployeeRole(employee_id, new_role_id)

        if not updated:
            raise LookupError("Empleado no encontrado")

        return True