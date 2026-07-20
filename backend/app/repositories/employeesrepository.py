from sqlalchemy.orm import Session
from app.models.employees import Employees

class EmployeeRepository:
    def __init__ (self,db:Session):
        self.db = db

    #crear empleados
    def registerEmployee(self, employee_data: dict) -> Employees:
        db_employee = Employees(**employee_data)
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee
    
    # Traer todos los empleados ordenados por nombre
    def getAllEmployees(self) -> list[Employees]:
        return self.db.query(Employees).order_by(Employees.name.asc()).all()

    # Buscar empleados filtrados por su rol
    def getEmployeesByRole(self, role_id: int) -> list[Employees]:
        return self.db.query(Employees).filter(Employees.role_id == role_id).order_by(Employees.name.asc()).all()

    #buscar empleado por nombre
    def get_employee_by_name(self, employeeName: str) -> Employees:
        return self.db.query(Employees).filter(Employees.name == employeeName).first()

    # Buscar empleado por ID
    def getEmployeeById(self, employee_id: int) -> Employees:
        return self.db.query(Employees).filter(Employees.id == employee_id).first()

    #actualizar empleados
    def update_employee(self, employeeName: str, new_data: dict) -> bool:
        db_employee = self.get_employee_by_name(employeeName)
        if db_employee:
            for key, value in new_data.items():
                setattr(db_employee, key, value)
            self.db.commit()
            return True
        return False

    #eliminar empleados
    def delete_employee(self, employeeName: str) -> bool:
        db_employee = self.get_employee_by_name(employeeName)
        if db_employee:
            self.db.delete(db_employee)
            self.db.commit()
            return True
        return False