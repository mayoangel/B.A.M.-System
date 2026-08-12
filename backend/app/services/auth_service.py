"""Autenticación unificada (RBAC): Empleados (Administrador/Docente) y
Tutores (Parents) inician sesión con el mismo endpoint, pero son entidades
independientes que viven en tablas distintas. El JWT resultante siempre
lleva el `role` normalizado ("admin" | "docente" | "tutor") y el
`actor_type` (tabla de origen), que son los dos claims que consume
`core/permissions.py` para autorizar cada petición.
"""
from flask_jwt_extended import create_access_token

from app.repositories.employees_repository import EmployeeRepository
from app.repositories.parents_repository import ParentRepository
from app.core.security import verify_password

ADMIN_ROLE_ID = 1


class AuthService:

    def __init__(self, db):
        self.employee_repository = EmployeeRepository(db)
        self.parent_repository = ParentRepository(db)

    @staticmethod
    def _role_for_employee(role_id: int) -> str:
        # El sistema solo distingue 2 niveles de acceso entre el personal:
        # Administrador, y todo el demás personal (Profesor/Prefecto) que
        # opera como "docente" para efectos de RBAC (toma de asistencia,
        # alta de alumnos en sus propios cursos).
        return "admin" if role_id == ADMIN_ROLE_ID else "docente"

    def login(self, email: str, password: str) -> dict | None:
        """Login unificado. Primero busca entre los Empleados (Administrador
        o Docente); si no hay coincidencia, busca entre los Tutores."""
        employee = self.employee_repository.getEmployeeByEmail(email)
        if employee and verify_password(password, employee.password):
            role = self._role_for_employee(employee.role_id)
            token = create_access_token(
                identity=str(employee.id),
                additional_claims={
                    "role": role,
                    "actor_type": "employee",
                    "role_id": employee.role_id,
                    "name": employee.name,
                },
            )
            return {
                "token": token,
                "id": employee.id,
                "name": employee.name,
                "role": role,
                "role_id": employee.role_id,
            }

        parent = self.parent_repository.get_parent_by_email(email)
        if parent and verify_password(password, parent.password):
            token = create_access_token(
                identity=str(parent.id),
                additional_claims={
                    "role": "tutor",
                    "actor_type": "parent",
                    "role_id": None,
                    "name": parent.name,
                },
            )
            return {
                "token": token,
                "id": parent.id,
                "name": parent.name,
                "role": "tutor",
                "role_id": None,
            }

        return None

    def get_profile(self, actor: dict) -> dict | None:
        if actor.get("actor_type") == "employee":
            employee = self.employee_repository.getEmployeeById(actor["id"])
            if not employee:
                return None
            return {
                "id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "role": self._role_for_employee(employee.role_id),
                "role_id": employee.role_id,
            }

        parent = self.parent_repository.get_parent_by_id(actor["id"])
        if not parent:
            return None
        return {
            "id": parent.id,
            "name": parent.name,
            "email": parent.email,
            "role": "tutor",
            "role_id": None,
        }

    def change_role(self, requester_role: str, employee_id: int, new_role_id: int) -> bool:
        if requester_role != "admin":
            raise PermissionError("Solo administradores pueden cambiar roles.")

        if not employee_id or not new_role_id:
            raise ValueError("employee_id y role_id son obligatorios")

        updated = self.employee_repository.updateEmployeeRole(employee_id, new_role_id)

        if not updated:
            raise LookupError("Empleado no encontrado")

        return True
