from sqlalchemy.orm import Session, joinedload
from app.models.students import Students
from app.models.student_courses import StudentCourses

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    # Crear estudiantes
    def registerStudent(self, student_data: dict) -> Students:
        db_student = Students(**student_data)
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student
    
    # Traer todos los estudiantes registrados
    def getAllStudents(self) -> list[Students]:
        return self.db.query(Students).order_by(Students.name.asc()).all()

    # Traer todos los estudiantes con su tutor y cursos precargados (evita
    # N+1 queries); usado por la pantalla de administración de alumnos.
    def get_all_students_with_relations(self) -> list[Students]:
        return (
            self.db.query(Students)
            .options(joinedload(Students.parent), joinedload(Students.courses))
            .order_by(Students.name.asc())
            .all()
        )

    # Traer estudiantes de un curso en específico a través de la tabla intermedia student_courses
    def getStudentsByCourse(self, course_id: int) -> list[Students]:
        return self.db.query(Students)\
            .join(StudentCourses, Students.id == StudentCourses.student_id)\
            .filter(StudentCourses.course_id == course_id)\
            .order_by(Students.name.asc()).all()

    # Buscar estudiante por nombre
    def getStudentByName(self, studentName: str) -> Students:
        return self.db.query(Students).filter(Students.name == studentName).first()

    # Buscar estudiante por Matrícula/Código único 
    def getStudentById(self, id_student: str) -> Students:
        return self.db.query(Students).filter(Students.id_student == id_student).first()

    # Cuenta cuántas matrículas ya existen con un prefijo dado (ej. "BAM-2026-"),
    # usado por StudentService para calcular la siguiente matrícula autogenerada.
    def count_students_with_prefix(self, prefix: str) -> int:
        return (
            self.db.query(Students)
            .filter(Students.id_student.like(f"{prefix}%"))
            .count()
        )

    # Buscar estudiante por su llave primaria interna (id autoincremental)
    def getStudentByPrimaryKey(self, student_pk: int) -> Students:
        return self.db.query(Students).filter(Students.id == student_pk).first()

    # Actualizar estudiantes
    def updateStudent(self, studentName: str, new_data: dict) -> bool:
        db_student = self.getStudentByName(studentName)
        if db_student:
            for key, value in new_data.items():
                setattr(db_student, key, value)
            self.db.commit()
            return True
        return False

    # Actualizar estudiantes por su llave primaria (usado por la pantalla de
    # administración, que trabaja con IDs numéricos en vez de nombres).
    def updateStudentByPrimaryKey(self, student_pk: int, new_data: dict) -> bool:
        db_student = self.getStudentByPrimaryKey(student_pk)
        if db_student:
            for key, value in new_data.items():
                setattr(db_student, key, value)
            self.db.commit()
            return True
        return False

    # Eliminar estudiantes
    def deleteStudents(self, studentName: str) -> bool:
        db_student = self.getStudentByName(studentName)
        if db_student:
            self.db.delete(db_student)
            self.db.commit()
            return True
        return False

    # Eliminar estudiantes por su llave primaria
    def deleteStudentByPrimaryKey(self, student_pk: int) -> bool:
        db_student = self.getStudentByPrimaryKey(student_pk)
        if db_student:
            self.db.delete(db_student)
            self.db.commit()
            return True
        return False