from sqlalchemy.orm import Session
from app.repositories.studentCourseRepository import StudentCoursesRepository  

class StudentCoursesService:
    def __init__(self, db: Session):
        self.repository = StudentCoursesRepository(db)

    def enroll_student_in_course(self, student_id: int, course_id: int) -> bool:
        if student_id <= 0 or course_id <= 0:
            raise ValueError("Los IDs de alumno y curso deben ser enteros positivos válidos.")
            
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