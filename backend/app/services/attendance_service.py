from sqlalchemy.orm import Session
from datetime import date, datetime
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.students_repository import StudentRepository
from app.repositories.employees_repository import EmployeeRepository
from app.repositories.employee_course_repository import EmployeeCourseRepository
from app.repositories.student_tutor_repository import StudentTutorRepository
from app.services.notification_service import NotificationService
from app.models.attendance import Attendance

class AttendanceServices:
    CRITICAL_ABSENCE_THRESHOLD = 3

    def __init__(self, db: Session):
        self.repo = AttendanceRepository(db)
        self.student_repo = StudentRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.employee_course_repo = EmployeeCourseRepository(db)
        self.student_tutor_repo = StudentTutorRepository(db)
        self.notification_service = NotificationService()

    # --- RBAC: helpers de autorización por fila (ver core/permissions.py) ---

    def _assert_can_access_course(self, course_id: int, actor: dict | None) -> None:
        if not actor or actor.get("role") == "admin":
            return
        if actor.get("role") == "docente":
            if not self.employee_course_repo.is_employee_assigned_to_course(actor["id"], course_id):
                raise PermissionError("Solo puedes acceder a la asistencia de cursos que impartes.")
            return
        raise PermissionError("No tienes permisos para acceder a la asistencia de este curso.")

    def _assert_can_access_student_attendance(self, student_id: int, actor: dict | None) -> None:
        if not actor or actor.get("role") == "admin":
            return
        if actor.get("role") == "docente":
            if not self.student_repo.is_student_in_employee_courses(student_id, actor["id"]):
                raise PermissionError("Solo puedes acceder a la asistencia de alumnos de tus cursos.")
            return
        if actor.get("role") == "tutor":
            student = self.student_repo.getStudentByPrimaryKey(student_id)
            if not student or student.id_parent != actor["id"]:
                raise PermissionError("Solo puedes acceder a la asistencia de tus propios hijos.")
            return
        raise PermissionError("No tienes permisos para acceder a esta asistencia.")

    def _parse_date(self, value):
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        raise ValueError("La fecha debe estar en formato YYYY-MM-DD")

    def _is_unjustified(self, status: str) -> bool:
        return isinstance(status, str) and status.strip().lower() == "falta injustificada"

    def _get_active_tutor(self, student_id: int):
        tutor_relation = self.student_tutor_repo.getActiveTutorByStudent(student_id)
        if tutor_relation:
            return self.employee_repo.getEmployeeById(tutor_relation.employee_id)
        return None

    def _get_admin_employees(self):
        return self.employee_repo.getAdminEmployees()

    def _notify_unjustified_absence(self, student_id: int, attendance_record: Attendance):
        student = self.student_repo.getStudentByPrimaryKey(student_id)
        if not student:
            return None

        tutor = self._get_active_tutor(student_id)
        if tutor:
            self.notification_service.notify_tutor_unjustified_absence(
                tutor,
                f"{student.name} {student.lastname}",
                str(attendance_record.date),
                attendance_record.course_id
            )

        total = self.repo.count_unjustified_absences_by_student(student_id)
        if total >= self.CRITICAL_ABSENCE_THRESHOLD:
            admins = self._get_admin_employees()
            self.notification_service.notify_admins_critical_absences(
                admins,
                f"{student.name} {student.lastname}",
                total
            )

        return {"student_id": student_id, "total_unjustified": total}

    def registerAttendances(self, attendance_data: dict, actor: dict | None = None):
        if not attendance_data.get('student_id'):
            raise ValueError("El ID del estudiante es obligatorio")
        if not attendance_data.get('status'):
            raise ValueError("El estatus es incorrecto u obligatorio")
        if not attendance_data.get('method'):
            raise ValueError("El método de asistencia es obligatorio")
        if not attendance_data.get('course_id'):
            raise ValueError("El curso (course_id) es obligatorio")

        # RBAC: un docente solo puede registrar asistencia para cursos que imparte.
        if actor and actor.get("role") == "docente":
            self._assert_can_access_course(attendance_data.get('course_id'), actor)

        if not attendance_data.get('date'):
            attendance_data['date'] = date.today()
        else:
            attendance_data['date'] = self._parse_date(attendance_data['date'])

        if not attendance_data.get('time'):
            attendance_data['time'] = datetime.now().time()

        student_exists = self.student_repo.getStudentByPrimaryKey(attendance_data.get('student_id'))
        if not student_exists:
            raise ValueError("El alumno ingresado no existe en el sistema")

        if attendance_data.get('employee_id'):
            employee_exists = self.employee_repo.getEmployeeById(attendance_data.get('employee_id'))
            if not employee_exists:
                raise ValueError("El empleado ingresado no existe en el sistema")

        # Unicidad por (alumno, fecha, curso): el mismo día puede asistir a
        # varias clases distintas, pero no duplicar la misma clase.
        asistencia_existente = self.repo.getStudentAttendanceByDateAndCourse(
            attendance_data.get('student_id'),
            attendance_data.get('date'),
            attendance_data.get('course_id'),
        )
        if asistencia_existente:
            raise ValueError(
                "El alumno ya tiene una asistencia registrada para este curso en esa fecha"
            )

        result = self.repo.registerAttendance(attendance_data)

        if self._is_unjustified(attendance_data.get('status')):
            self._notify_unjustified_absence(attendance_data.get('student_id'), result)

        return result

    def getAttendanceByStudent(self, student_id: int, actor: dict | None = None):
        self._assert_can_access_student_attendance(student_id, actor)
        return self.repo.getAttendanceByStudent(student_id)

    def getAttendanceByStudentAndDate(self, student_id: int, target_date, actor: dict | None = None):
        self._assert_can_access_student_attendance(student_id, actor)
        parsed_date = self._parse_date(target_date)
        return self.repo.getAttendanceByStudentAndDate(student_id, parsed_date)

    def getAttendanceByCourseAndDate(self, course_id: int, target_date, actor: dict | None = None):
        self._assert_can_access_course(course_id, actor)
        parsed_date = self._parse_date(target_date)
        return self.repo.getAttendanceByCourseAndDate(course_id, parsed_date)

    def getAttendanceByCourseAndDateRange(self, course_id: int, start_date, end_date, actor: dict | None = None):
        self._assert_can_access_course(course_id, actor)
        start = self._parse_date(start_date)
        end = self._parse_date(end_date)
        return self.repo.getAttendanceByCourseAndDateRange(course_id, start, end)

    def getStudentAttendanceByDate(self, student_id: int, target_date: date):
        return self.repo.getStudentAttendanceByDate(student_id, target_date)

    def get_critical_absence_alerts(self, threshold: int | None = None):
        threshold = threshold or self.CRITICAL_ABSENCE_THRESHOLD
        rows = self.repo.get_unjustified_absence_counts(threshold)

        alerts = []
        for student_id, unjustified_count in rows:
            student = self.student_repo.getStudentByPrimaryKey(student_id)
            alerts.append({
                "student_id": student_id,
                "student_name": f"{student.name} {student.lastname}" if student else None,
                "unjustified_absences": unjustified_count
            })
        return alerts

    def modificar_asistencia_por_fecha(self, student_id: int, fecha_str: str, nuevos_datos: dict):
        try:
            fecha_objeto = self._parse_date(fecha_str)
        except ValueError:
            raise ValueError("El formato de la fecha debe ser YYYY-MM-DD")

        exito = self.repo.updateAttendanceByStudentAndDate(student_id, fecha_objeto, nuevos_datos)
        if not exito:
            raise ValueError(f"No se encontró ningún registro de asistencia para el alumno en la fecha {fecha_str}")
        return exito