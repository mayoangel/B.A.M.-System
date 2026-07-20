from sqlalchemy.orm import Session
from app.repositories.employeeCourseRepository import EmployeeCourseRepository

class EmployeeCourseService:
    def __init__(self, db: Session):
        self.repository = EmployeeCourseRepository(db)

    def assign_course_to_employee(self, employee_id: int, course_id: int) -> bool:
        success = self.repository.assignCourseToEmployee(employee_id, course_id)
        if not success:
            raise ValueError(
                "No se pudo asignar el curso al empleado. "
                "Verifica si el curso ya está asignado o si los IDs son válidos."
            )
        return True

    def remove_course_from_employee(self, employee_id: int, course_id: int) -> bool:
        success = self.repository.removeCourseFromEmployee(employee_id, course_id)
        if not success:
            raise ValueError("No se pudo retirar el curso. Verifica si la asignación existía en la base de datos.")
        return True