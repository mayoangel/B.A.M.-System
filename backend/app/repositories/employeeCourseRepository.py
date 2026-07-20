from sqlalchemy.orm import Session
from app.models.employee_course import EmployeeCourse

class EmployeeCourseRepository:
    def __init__(self, db: Session):
        self.db = db

    # Asignar un curso/materia a un empleado/docente
    def assignCourseToEmployee(self, employee_id: int, course_id: int) -> bool:
        try:
            db_association = EmployeeCourse(employee_id=employee_id, course_id=course_id)
            self.db.add(db_association)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    # Retirar un curso a un docente
    def removeCourseFromEmployee(self, employee_id: int, course_id: int) -> bool:
        query = self.db.query(EmployeeCourse).filter(
            EmployeeCourse.employee_id == employee_id, 
            EmployeeCourse.course_id == course_id
        )
        db_association = query.first()
        if db_association:
            self.db.delete(db_association)
            self.db.commit()
            return True
        return False