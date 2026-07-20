from sqlalchemy.orm import Session
from app.models.student_courses import StudentCourses

class StudentCoursesRepository:
    def __init__(self, db: Session):
        self.db = db

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