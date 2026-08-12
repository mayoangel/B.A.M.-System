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

    def get_course_by_id(self, course_id: int) -> Courses:
        return self.db.query(Courses).filter(Courses.id == course_id).first()
    
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

    # Baja lógica por ID (preferible al nombre: evita romper URLs con "/" en el nombre).
    def deactivate_course_by_id(self, course_id: int) -> Courses | None:
        db_course = self.get_course_by_id(course_id)
        if not db_course:
            return None
        if db_course.status != "Inactivo":
            db_course.status = "Inactivo"
            self.db.commit()
        return db_course

    def activate_course_by_id(self, course_id: int) -> Courses | None:
        db_course = self.get_course_by_id(course_id)
        if not db_course:
            return None
        if db_course.status != "Activo":
            db_course.status = "Activo"
            self.db.commit()
        return db_course

    # Baja lógica: el curso no se borra de la BD (conserva historial de
    # asistencias e inscripciones); solo pasa a "Inactivo".
    def deactivate_course(self, courseName: str) -> bool:
        db_course = self.get_course_by_name(courseName)
        if not db_course:
            return False
        if db_course.status == "Inactivo":
            return True
        db_course.status = "Inactivo"
        self.db.commit()
        return True

    def activate_course(self, courseName: str) -> bool:
        db_course = self.get_course_by_name(courseName)
        if not db_course:
            return False
        if db_course.status == "Activo":
            return True
        db_course.status = "Activo"
        self.db.commit()
        return True
