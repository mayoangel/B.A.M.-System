from sqlalchemy.orm import Session, joinedload
from app.models.students import Students
from app.models.student_courses import StudentCourses
from app.models.employee_course import EmployeeCourse

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

    # RBAC (Tutor): hijos de un tutor específico, con tutor/cursos precargados.
    def get_students_with_relations_by_parent(self, parent_id: int) -> list[Students]:
        return (
            self.db.query(Students)
            .options(joinedload(Students.parent), joinedload(Students.courses))
            .filter(Students.id_parent == parent_id)
            .order_by(Students.name.asc())
            .all()
        )

    # RBAC (Docente): alumnos inscritos en cualquiera de los cursos que
    # imparte el docente, con tutor/cursos precargados. `distinct()` evita
    # duplicados cuando un alumno comparte varios cursos con el mismo docente.
    def get_students_with_relations_by_employee(self, employee_id: int) -> list[Students]:
        return (
            self.db.query(Students)
            .options(joinedload(Students.parent), joinedload(Students.courses))
            .join(StudentCourses, StudentCourses.student_id == Students.id)
            .join(EmployeeCourse, EmployeeCourse.course_id == StudentCourses.course_id)
            .filter(EmployeeCourse.employee_id == employee_id)
            .order_by(Students.name.asc())
            .distinct()
            .all()
        )

    # RBAC (Docente): ¿el alumno está inscrito en algún curso que imparte este docente?
    def is_student_in_employee_courses(self, student_id: int, employee_id: int) -> bool:
        return (
            self.db.query(StudentCourses)
            .join(EmployeeCourse, EmployeeCourse.course_id == StudentCourses.course_id)
            .filter(
                StudentCourses.student_id == student_id,
                EmployeeCourse.employee_id == employee_id,
            )
            .first()
            is not None
        )

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