
######### LO AGREGUE PARA EL REQUIRIEMIENTO 5   ##########

from flask_jwt_extended import create_access_token
from app.models.employees import Employees
from app.core.security import verify_password


class AuthService:

    def __init__(self, db):
        self.db = db

    def login(self, email, password):

        employee = (
            self.db.query(Employees)
            .filter(Employees.email == email)
            .first()
        )

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