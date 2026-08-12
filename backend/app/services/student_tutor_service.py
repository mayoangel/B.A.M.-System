from sqlalchemy.orm import Session
from app.repositories.student_tutor_repository import StudentTutorRepository
from app.models.student_tutor import StudentTutor

class StudentTutorService:
    def __init__(self, db: Session):
        self.repository = StudentTutorRepository(db)

    def assign_tutor(self, assignment_data: dict) -> StudentTutor:
        # Lógica de negocio: Verificar campos mandatorios
        student_id = assignment_data.get("student_id")
        employee_id = assignment_data.get("employee_id")
        
        if not student_id or not employee_id:
            raise ValueError("Tanto 'student_id' como 'employee_id' son obligatorios para la asignación.")

        existing_active_tutor = self.repository.getActiveTutorByStudent(student_id)
        if existing_active_tutor:
            raise ValueError(
                f"El estudiante con ID {student_id} ya tiene un tutor activo asignado "
                f"(ID de Empleado/Docente: {existing_active_tutor.employee_id}). "
                "Por favor, da de baja la relación actual antes de asignar uno nuevo."
            )

        if not assignment_data.get("status"):
            assignment_data["status"] = "Activo"

        return self.repository.assignTutor(assignment_data)

    def get_active_tutor_by_student(self, student_id: int) -> StudentTutor:
        if student_id <= 0:
            raise ValueError("El ID del estudiante debe ser un número entero positivo.")
            
        active_tutor = self.repository.getActiveTutorByStudent(student_id)
        if not active_tutor:
            raise ValueError(f"No se encontró ningún tutor activo para el estudiante con ID {student_id}.")
        return active_tutor