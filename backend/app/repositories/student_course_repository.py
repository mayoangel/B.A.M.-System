from sqlalchemy.orm import Session
from app.models.student_courses import StudentCourses
from app.models.courses import Courses

class StudentCoursesRepository:
    def __init__(self, db: Session):
        self.db = db

    # Cursos en los que está inscrito un alumno; usado por la pantalla de
    # administración para preseleccionar el curso actual en el modal de edición.
    def get_courses_by_student(self, student_id: int) -> list[Courses]:
        return (
            self.db.query(Courses)
            .join(StudentCourses, StudentCourses.course_id == Courses.id)
            .filter(StudentCourses.student_id == student_id)
            .all()
        )

    def is_student_enrolled(self, student_id: int, course_id: int) -> bool:
        return self.db.query(StudentCourses).filter(
            StudentCourses.student_id == student_id,
            StudentCourses.course_id == course_id
        ).first() is not None

    def enrollStudentInCourse(self, student_id: int, course_id: int) -> bool:
        try:
            if self.is_student_enrolled(student_id, course_id):
                return False
            
            new_enrollment = StudentCourses(student_id=student_id, course_id=course_id)
            self.db.add(new_enrollment)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def removeStudentFromCourse(self, student_id: int, course_id: int) -> bool:
        try:
            enrollment = self.db.query(StudentCourses).filter(
                StudentCourses.student_id == student_id,
                StudentCourses.course_id == course_id
            ).first()

            if not enrollment:
                return False

            self.db.delete(enrollment)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False