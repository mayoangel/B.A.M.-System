from sqlalchemy.orm import Session
from app.repositories.student_course_repository import StudentCoursesRepository
from app.repositories.employee_course_repository import EmployeeCourseRepository

class StudentCoursesService:
    def __init__(self, db: Session):
        self.repository = StudentCoursesRepository(db)
        self.employee_course_repository = EmployeeCourseRepository(db)

    def get_courses_for_student(self, student_id: int) -> list:
        if student_id <= 0:
            raise ValueError("El ID del alumno debe ser un entero positivo válido.")
        return self.repository.get_courses_by_student(student_id)

    def enroll_student_in_course(self, student_id: int, course_id: int, actor: dict | None = None) -> bool:
        if student_id <= 0 or course_id <= 0:
            raise ValueError("Los IDs de alumno y curso deben ser enteros positivos válidos.")

        # RBAC: un docente solo puede inscribir alumnos en un curso que imparte.
        if actor and actor.get("role") == "docente":
            if not self.employee_course_repository.is_employee_assigned_to_course(actor["id"], course_id):
                raise PermissionError("Solo puedes inscribir alumnos en un curso que impartes.")

        success = self.repository.enrollStudentInCourse(student_id, course_id)
        if not success:
            raise ValueError("No se pudo inscribir al alumno. Es posible que ya se encuentre inscrito en este curso o que los registros no existan.")
        return True

    def remove_student_from_course(self, student_id: int, course_id: int) -> bool:
        if student_id <= 0 or course_id <= 0:
            raise ValueError("Los IDs de alumno y curso deben ser enteros positivos válidos.")

        success = self.repository.removeStudentFromCourse(student_id, course_id)
        if not success:
            raise ValueError("No se pudo proceder con la baja. Verifica si el alumno realmente pertenecía a ese curso.")
        return True