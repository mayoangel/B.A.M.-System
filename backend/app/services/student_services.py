from sqlalchemy.orm import Session
from app.repositories.studentsrepository import StudentRepository
from app.models.students import Students

class StudentService:
    def __init__(self, db: Session):
        self.repository = StudentRepository(db)

    def register_student(self, student_data: dict) -> Students:
        if not student_data.get("id_student") or not student_data.get("name"):
            raise ValueError("La matrícula (id_student) y el nombre son campos obligatorios.")
            
        existing_code = self.repository.getStudentById(student_data.get("id_student"))
        if existing_code:
            raise ValueError(f"Ya existe un estudiante registrado con la matrícula '{student_data.get('id_student')}'.")

        existing_name = self.repository.getStudentByName(student_data.get("name"))
        if existing_name:
            raise ValueError("Ya existe un estudiante registrado con ese nombre.")
            
        return self.repository.registerStudent(student_data)
    
    def list_all_students(self) -> list[Students]:
        return self.repository.getAllStudents()

    def list_students_by_course(self, course_id: int) -> list[Students]:
        if not course_id:
            raise ValueError("El identificador del curso (course_id) es obligatorio.")
        return self.repository.getStudentsByCourse(course_id)

    def get_student_by_name(self, student_name: str) -> Students:
        student = self.repository.getStudentByName(student_name)
        if not student:
            raise ValueError(f"El estudiante '{student_name}' no fue encontrado.")
        return student

    def update_student(self, student_name: str, new_data: dict) -> bool:
        updated = self.repository.updateStudent(student_name, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: El estudiante '{student_name}' no existe.")
        return True

    def delete_student(self, student_name: str) -> bool:
        deleted = self.repository.deleteStudents(student_name)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: El estudiante '{student_name}' no existe.")
        return True