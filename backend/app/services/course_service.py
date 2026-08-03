from sqlalchemy.orm import Session
from app.repositories.courses_repository import CourseRepository
from app.repositories.employee_course_repository import EmployeeCourseRepository
from app.models.courses import Courses

class CourseService:
    def __init__(self, db: Session):
        self.repository = CourseRepository(db)
        self.employee_course_repository = EmployeeCourseRepository(db)

    def register_course(self, course_data: dict) -> Courses:
        existing = self.repository.get_course_by_name(course_data.get("name"))
        if existing:
            raise ValueError("Ya existe un curso registrado con ese nombre.")
        return self.repository.registerCourse(course_data)
    
    def get_all_courses(self):
        return self.repository.get_all_courses()

    def get_active_courses(self, actor: dict | None = None):
        """RBAC: un docente solo debe ver, en los selectores de curso (alta de
        alumnos, pase de lista), los cursos que él mismo imparte."""
        if actor and actor.get("role") == "docente":
            return [
                course
                for course in self.employee_course_repository.get_courses_by_employee(actor["id"])
                if course.status == "Activo"
            ]
        return self.repository.get_active_courses()

    def get_course_by_name(self, course_name: str) -> Courses:
        course = self.repository.get_course_by_name(course_name)
        if not course:
            raise ValueError(f"El curso '{course_name}' no fue encontrado.")
        return course

    def update_course(self, course_name: str, new_data: dict) -> bool:
        updated = self.repository.update_course(course_name, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: El curso '{course_name}' no existe.")
        return True

    def delete_course(self, course_name: str) -> bool:
        deleted = self.repository.delete_course(course_name)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: El curso '{course_name}' no existe.")
        return True