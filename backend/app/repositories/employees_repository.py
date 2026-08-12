from sqlalchemy.orm import Session
from app.models.employees import Employees
from app.models.role import Role

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

    # Buscar empleado por correo electrónico (usado para autenticación)
    def getEmployeeByEmail(self, email: str) -> Employees:
        return self.db.query(Employees).filter(Employees.email == email).first()

    # Actualizar únicamente el rol de un empleado
    def updateEmployeeRole(self, employee_id: int, new_role_id: int) -> bool:
        db_employee = self.getEmployeeById(employee_id)
        if db_employee:
            db_employee.role_id = new_role_id
            self.db.commit()
            return True
        return False

    # Traer empleados con rol administrativo; si no hay ninguno, cae a los empleados activos
    def getAdminEmployees(self) -> list[Employees]:
        admins = (
            self.db.query(Employees)
            .join(Role, Employees.role_id == Role.id)
            .filter(Role.name.ilike("%admin%") | Role.name.ilike("%administrador%"))
            .all()
        )
        if not admins:
            admins = self.db.query(Employees).filter(Employees.status == "Activo").all()
        return admins

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