from app.models.employees import Employees

class NotificationService:
    def notify_tutor_unjustified_absence(self, tutor: Employees, student_name: str, absence_date: str, course_id: int):
        message = (
            f"Tutor {tutor.name} {tutor.lastname}, el estudiante {student_name} "
            f"tiene una falta injustificada el {absence_date} en el curso {course_id}."
        )
        print("[NOTIFICACIÓN TUTOR]", message)
        return {"recipient": tutor.email, "message": message}

    def notify_admins_critical_absences(self, admins: list[Employees], student_name: str, total_absences: int):
        messages = []
        for admin in admins:
            message = (
                f"Administrador {admin.name} {admin.lastname}, el estudiante {student_name} "
                f"tiene {total_absences} faltas injustificadas, estado crítico."
            )
            print("[ALERTA ADMIN]", message)
            messages.append({"recipient": admin.email, "message": message})
        return messages