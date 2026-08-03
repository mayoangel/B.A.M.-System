from sqlalchemy.orm import Session
from app.models.courses import Courses

class CourseRepository:
    def __init__ (self,db:Session):
        self.db = db

    #crear cursos
    def registerCourse(self, course_data: dict) -> Courses:
        db_course = Courses(**course_data)
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    #buscar curso por nombre
    def get_course_by_name(self, courseName: str) -> Courses:
        return self.db.query(Courses).filter(Courses.name == courseName).first()
    
     # Traer todos los cursos
    def get_all_courses(self):
        return self.db.query(Courses).all()

    # Traer solo los cursos activos
    def get_active_courses(self):
        return self.db.query(Courses).filter(Courses.status == "Activo").all()

    #actualizar cursos
    def update_course(self, courseName: str, new_data: dict) -> bool:
        db_course = self.get_course_by_name(courseName)
        if db_course:
            for key, value in new_data.items():
                setattr(db_course, key, value)
            self.db.commit()
            return True
        return False

    #eliminar cursos
    def delete_course(self, courseName: str) -> bool:
        db_course = self.get_course_by_name(courseName)
        if db_course:
            self.db.delete(db_course)
            self.db.commit()
            return True
        return False