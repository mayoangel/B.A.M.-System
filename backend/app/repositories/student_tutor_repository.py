from sqlalchemy.orm import Session
from app.models.student_tutor import StudentTutor

class StudentTutorRepository:
    def __init__(self, db: Session):
        self.db = db

    # Vincular un alumno con un docente/tutor responsable
    def assignTutor(self, assignment_data: dict) -> StudentTutor:
        db_assignment = StudentTutor(**assignment_data)
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment

    # Buscar relación activa por ID de estudiante (la más reciente si hubiera varias)
    def getActiveTutorByStudent(self, student_id: int) -> StudentTutor:
        return self.db.query(StudentTutor).filter(
            StudentTutor.student_id == student_id, 
            StudentTutor.status == "Activo"
        ).order_by(StudentTutor.start_date.desc()).first()