from sqlalchemy.orm import Session
from app.repositories.employeesrepository import EmployeeRepository  
from app.models.employees import Employees

class EmployeeService:
    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)

    def register_employee(self, employee_data: dict) -> Employees:
        if not employee_data.get("name") or not employee_data.get("email"):
            raise ValueError("El nombre y el correo electrónico son obligatorios.")

        existing = self.repository.get_employee_by_name(employee_data.get("name"))
        if existing:
            raise ValueError("Ya existe un empleado registrado con ese nombre.")
        return self.repository.registerEmployee(employee_data)
    
    def list_all_employees(self) -> list[Employees]:
        return self.repository.getAllEmployees()

    def get_employees_by_role(self, role_id: int) -> list[Employees]:
        if not role_id:
            raise ValueError("El identificador del rol es obligatorio.")
        return self.repository.getEmployeesByRole(role_id)

    def get_employee_by_name(self, employee_name: str) -> Employees:
        employee = self.repository.get_employee_by_name(employee_name)
        if not employee:
            raise ValueError(f"El empleado '{employee_name}' no existe.")
        return employee

    def update_employee(self, employee_name: str, new_data: dict) -> bool:
        updated = self.repository.update_employee(employee_name, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: El empleado '{employee_name}' no existe.")
        return True

    def delete_employee(self, employee_name: str) -> bool:
        deleted = self.repository.delete_employee(employee_name)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: El empleado '{employee_name}' no existe.")
        return True