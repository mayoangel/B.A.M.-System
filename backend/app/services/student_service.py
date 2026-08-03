from datetime import datetime

from sqlalchemy.orm import Session
from app.repositories.students_repository import StudentRepository
from app.models.students import Students

MATRICULA_PREFIX_TEMPLATE = "BAM-{year}-"
MATRICULA_SEQUENCE_DIGITS = 4


class StudentService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = StudentRepository(db)

    def register_student(self, student_data: dict) -> Students:
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
        # La matrícula SIEMPRE la genera el sistema: se ignora cualquier valor
        # de `id_student` que haya llegado en el payload (el alumno es menor
        # de edad y no debe poder auto-asignarse un identificador).
        student_data["id_student"] = self._generate_matricula()

        return self.repository.registerStudent(student_data)

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

    def list_all_students_detailed(self) -> list[Students]:
        """Alumnos con su tutor y cursos precargados, para la pantalla de
        administración (tabla con búsqueda/filtros por curso o estatus)."""
        return self.repository.get_all_students_with_relations()

    def list_students_by_course(self, course_id: int) -> list[Students]:
        if not course_id:
            raise ValueError("El identificador del curso (course_id) es obligatorio.")
        return self.repository.getStudentsByCourse(course_id)

    def get_student_by_name(self, student_name: str) -> Students:
        student = self.repository.getStudentByName(student_name)
        if not student:
            raise ValueError(f"El estudiante '{student_name}' no fue encontrado.")
        return student

    def get_student_by_id(self, student_pk: int) -> Students:
        student = self.repository.getStudentByPrimaryKey(student_pk)
        if not student:
            raise ValueError(f"No se encontró al alumno con ID {student_pk}.")
        return student

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
