import { apiDelete, apiGet, apiPostJson, apiPutJson } from './client.js'

/**
 * Crea un alumno nuevo. `payload` debe respetar `StudentSchema`
 * (backend/app/schemas/students.py): name, lastname, surename?,
 * date_of_birth, id_parent. La matrícula (`id_student`) la genera el
 * backend automáticamente.
 */
export function createStudent(payload) {
  return apiPostJson('/students/', payload)
}

/** Lista los alumnos inscritos en un curso (usado en el pase de lista). */
export function getStudentsByCourse(courseId) {
  return apiGet(`/students/course/${courseId}`)
}

/**
 * Lista completa de alumnos con su tutor y cursos embebidos (usado en la
 * pantalla de Administración de Alumnos: tabla, búsqueda y filtros).
 */
export function getAllStudentsDetailed() {
  return apiGet('/students/')
}

/** Expediente completo de un alumno por su ID numérico interno. */
export function getStudentById(studentId) {
  return apiGet(`/students/id/${studentId}`)
}

/** Actualiza los datos de un alumno (parcial) por su ID numérico interno. */
export function updateStudent(studentId, payload) {
  return apiPutJson(`/students/id/${studentId}`, payload)
}

/**
 * Da de baja a un alumno. El backend elimina también, de forma permanente,
 * su información biométrica (fila en BD y caché en memoria), conforme a la
 * LFPDPPP.
 */
export function deleteStudent(studentId) {
  return apiDelete(`/students/id/${studentId}`)
}
