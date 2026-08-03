from datetime import datetime

from sqlalchemy.orm import Session
from app.repositories.students_repository import StudentRepository
from app.repositories.employee_course_repository import EmployeeCourseRepository
from app.repositories.student_course_repository import StudentCoursesRepository
from app.models.students import Students

MATRICULA_PREFIX_TEMPLATE = "BAM-{year}-"
MATRICULA_SEQUENCE_DIGITS = 4


class StudentService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = StudentRepository(db)
        self.employee_course_repository = EmployeeCourseRepository(db)
        self.student_course_repository = StudentCoursesRepository(db)

    def register_student(self, student_data: dict, actor: dict | None = None) -> Students:
        if not student_data.get("name") or not student_data.get("lastname"):
            raise ValueError("El nombre y el apellido paterno son campos obligatorios.")

        if not student_data.get("date_of_birth"):
            raise ValueError("La fecha de nacimiento es obligatoria.")

        if not student_data.get("id_parent"):
            raise ValueError("Se requiere el ID del tutor (id_parent) para registrar al alumno.")

        existing_name = self.repository.getStudentByName(student_data.get("name"))
        if existing_name:
            raise ValueError("Ya existe un estudiante registrado con ese nombre.")

        student_data = dict(student_data)
        # `course_id` no es un campo de la entidad Students: solo se usa aquí
        # para decidir la inscripción (ver RBAC de Docente más abajo).
        requested_course_id = student_data.pop("course_id", None)

        # RBAC: si un Docente registra a un alumno indicando un curso (ya sea
        # en este mismo payload, o después mediante /enrollments/enroll), esa
        # asignación solo puede ser a un curso que él mismo imparte. La
        # inscripción real puede llegar en esta misma petición (`course_id`)
        # o en una petición posterior de inscripción; ambos puntos de entrada
        # validan la pertenencia del curso al docente.
        if actor and actor.get("role") == "docente" and requested_course_id:
            if not self.employee_course_repository.is_employee_assigned_to_course(
                actor["id"], requested_course_id
            ):
                raise ValueError(
                    "Solo puedes registrar alumnos en un curso que impartes."
                )

        # La matrícula SIEMPRE la genera el sistema: se ignora cualquier valor
        # de `id_student` que haya llegado en el payload (el alumno es menor
        # de edad y no debe poder auto-asignarse un identificador).
        student_data["id_student"] = self._generate_matricula()

        student = self.repository.registerStudent(student_data)

        if requested_course_id:
            self.student_course_repository.enrollStudentInCourse(student.id, requested_course_id)

        return student

    def _generate_matricula(self) -> str:
        """Genera la siguiente matrícula disponible con formato BAM-<año>-<secuencia>.

        Ej.: BAM-2026-0001, BAM-2026-0002, ...
        """
        prefix = MATRICULA_PREFIX_TEMPLATE.format(year=datetime.now().year)
        sequence = self.repository.count_students_with_prefix(prefix) + 1
        candidate = f"{prefix}{sequence:0{MATRICULA_SEQUENCE_DIGITS}d}"

        # Defensivo: si ya existe (ej. por una baja previa), avanza la
        # secuencia hasta encontrar una matrícula realmente libre.
        while self.repository.getStudentById(candidate):
            sequence += 1
            candidate = f"{prefix}{sequence:0{MATRICULA_SEQUENCE_DIGITS}d}"

        return candidate

    def list_all_students(self) -> list[Students]:
        return self.repository.getAllStudents()

    def list_all_students_detailed(self, actor: dict | None = None) -> list[Students]:
        """Alumnos con su tutor y cursos precargados, para la pantalla de
        administración de alumnos. El resultado se filtra según el rol del
        actor autenticado (RBAC):
          - admin: todos los alumnos.
          - docente: solo alumnos inscritos en cursos que imparte.
          - tutor: solo sus propios hijos.
        """
        if not actor or actor.get("role") == "admin":
            return self.repository.get_all_students_with_relations()

        if actor.get("role") == "docente":
            return self.repository.get_students_with_relations_by_employee(actor["id"])

        if actor.get("role") == "tutor":
            return self.repository.get_students_with_relations_by_parent(actor["id"])

        return []

    def list_students_by_course(self, course_id: int, actor: dict | None = None) -> list[Students]:
        if not course_id:
            raise ValueError("El identificador del curso (course_id) es obligatorio.")

        if actor and actor.get("role") == "docente":
            if not self.employee_course_repository.is_employee_assigned_to_course(
                actor["id"], course_id
            ):
                raise PermissionError("Solo puedes consultar alumnos de un curso que impartes.")

        return self.repository.getStudentsByCourse(course_id)

    def get_student_by_name(self, student_name: str) -> Students:
        student = self.repository.getStudentByName(student_name)
        if not student:
            raise ValueError(f"El estudiante '{student_name}' no fue encontrado.")
        return student

    def get_student_by_id(self, student_pk: int, actor: dict | None = None) -> Students:
        student = self.repository.getStudentByPrimaryKey(student_pk)
        if not student:
            raise ValueError(f"No se encontró al alumno con ID {student_pk}.")

        self._assert_can_access_student(student, actor)
        return student

    def assert_actor_can_access_student(self, student_pk: int, actor: dict | None) -> Students:
        """Punto de entrada usado por otros servicios (ej. biométrico) para
        validar, antes de operar sobre un alumno, que el actor autenticado
        tiene permiso de acceso según las reglas de RBAC."""
        return self.get_student_by_id(student_pk, actor)

    def _assert_can_access_student(self, student: Students, actor: dict | None) -> None:
        if not actor or actor.get("role") == "admin":
            return

        if actor.get("role") == "docente":
            # Un alumno recién creado (ej. durante el flujo de registro, antes
            # de que se complete su inscripción a curso) todavía no pertenece
            # a ningún curso: se permite el acceso para no romper ese flujo.
            # Una vez que el alumno ya está inscrito en algún curso, solo los
            # docentes de ese curso pueden seguir accediendo a él.
            if student.courses and not self.repository.is_student_in_employee_courses(
                student.id, actor["id"]
            ):
                raise PermissionError(
                    "Solo puedes acceder a alumnos inscritos en cursos que impartes."
                )
            return

        if actor.get("role") == "tutor":
            if student.id_parent != actor["id"]:
                raise PermissionError("Solo puedes acceder a la información de tus propios hijos.")
            return

        raise PermissionError("No tienes permisos para acceder a este alumno.")

    def update_student(self, student_name: str, new_data: dict) -> bool:
        new_data = dict(new_data)
        # La matrícula no es editable manualmente una vez generada.
        new_data.pop("id_student", None)

        updated = self.repository.updateStudent(student_name, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: El estudiante '{student_name}' no existe.")
        return True

    def update_student_by_id(self, student_pk: int, new_data: dict) -> bool:
        new_data = dict(new_data)
        new_data.pop("id_student", None)

        updated = self.repository.updateStudentByPrimaryKey(student_pk, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: no existe un alumno con ID {student_pk}.")
        return True

    def delete_student(self, student_name: str) -> bool:
        student = self.repository.getStudentByName(student_name)
        if not student:
            raise ValueError(f"No se pudo eliminar: El estudiante '{student_name}' no existe.")

        self._purge_biometric_data(student.id)
        self.repository.deleteStudents(student_name)
        return True

    def delete_student_by_id(self, student_pk: int) -> bool:
        student = self.repository.getStudentByPrimaryKey(student_pk)
        if not student:
            raise ValueError(f"No se pudo eliminar: no existe un alumno con ID {student_pk}.")

        self._purge_biometric_data(student.id)
        self.repository.deleteStudentByPrimaryKey(student_pk)
        return True

    def _purge_biometric_data(self, student_id: int) -> None:
        """LFPDPPP: al dar de baja a un alumno, su vector biométrico debe
        eliminarse de forma permanente. No basta con dejar que el `CASCADE`
        de la base de datos borre la fila: también hay que limpiar la caché
        en memoria del motor de reconocimiento, así que se pasa siempre por
        `BiometricService.delete_biometric` en vez de confiar solo en SQL.
        """
        # Import perezoso para evitar cargar el motor de reconocimiento facial
        # (InsightFace/ONNX) en operaciones que nunca lo necesitan.
        from app.services.biometric_service import BiometricService

        try:
            BiometricService(self.db).delete_biometric(student_id)
        except ValueError:
            # El alumno no tenía información biométrica registrada: no hay nada que purgar.
            pass
