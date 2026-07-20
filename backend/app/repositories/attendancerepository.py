from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from datetime import date

class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    # Registrar asistencia
    def registerAttendance(self, attendance_data: dict) -> Attendance:
        db_attendance = Attendance(**attendance_data)
        self.db.add(db_attendance)
        self.db.commit()
        self.db.refresh(db_attendance)
        return db_attendance

    # Obtener historial de asistencias de un alumno
    def getAttendanceByStudent(self, student_id: int):
        return self.db.query(Attendance).filter(Attendance.student_id == student_id).all()

    # Obtener asistencias de un alumno en una fecha específica
    def getStudentAttendanceByDate(self, student_id: int, current_date: date):
        return self.db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.date == current_date
        ).first()

    # Obtener todas las asistencias de un alumno en una fecha específica
    def getAttendanceByStudentAndDate(self, student_id: int, current_date: date):
        return self.db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.date == current_date
        ).all()

    # Obtener asistencias por curso en una fecha específica
    def getAttendanceByCourseAndDate(self, course_id: int, current_date: date):
        return self.db.query(Attendance).filter(
            Attendance.course_id == course_id,
            Attendance.date == current_date
        ).all()

    # Obtener asistencias por curso en un rango de fechas
    def getAttendanceByCourseAndDateRange(self, course_id: int, start_date: date, end_date: date):
        return self.db.query(Attendance).filter(
            Attendance.course_id == course_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).order_by(Attendance.date.asc(), Attendance.time.asc()).all()

    # Actualizar la información de una asistencia
    def updateAttendanceByStudentAndDate(self, student_id: int, target_date: date, new_data: dict) -> bool:
        db_attendance = self.getStudentAttendanceByDate(student_id, target_date)

        if db_attendance:
            for key, value in new_data.items():
                setattr(db_attendance, key, value)
            self.db.commit()
            return True
        return False
    
    # Contar inasistencias injustificadas de un alumno
    def count_unjustified_absences_by_student(self, student_id: int) -> int:
        return self.db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.status == "Falta injustificada"
        ).count()