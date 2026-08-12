from sqlalchemy.orm import Session
from app.models.employee_course import EmployeeCourse
from app.models.employees import Employees
from app.models.courses import Courses

class EmployeeCourseRepository:
    def __init__(self, db: Session):
        self.db = db

    # Empleados/docentes asignados a un curso (para mostrar el maestro en el
    # pase de lista). Un curso puede tener varios; el service decide cuál
    # mostrar como "titular".
    def get_employees_by_course(self, course_id: int) -> list[Employees]:
        return (
            self.db.query(Employees)
            .join(EmployeeCourse, EmployeeCourse.employee_id == Employees.id)
            .filter(EmployeeCourse.course_id == course_id)
            .order_by(Employees.name.asc())
            .all()
        )

    # RBAC (Docente): cursos que imparte un docente específico (para filtrar
    # el selector de "Pase de Lista" y el alta de alumnos a su propio curso).
    def get_courses_by_employee(self, employee_id: int) -> list[Courses]:
        return (
            self.db.query(Courses)
            .join(EmployeeCourse, EmployeeCourse.course_id == Courses.id)
            .filter(EmployeeCourse.employee_id == employee_id)
            .order_by(Courses.name.asc())
            .all()
        )

    # RBAC (Docente): ¿este docente imparte este curso?
    def is_employee_assigned_to_course(self, employee_id: int, course_id: int) -> bool:
        return (
            self.db.query(EmployeeCourse)
            .filter(
                EmployeeCourse.employee_id == employee_id,
                EmployeeCourse.course_id == course_id,
            )
            .first()
            is not None
        )

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