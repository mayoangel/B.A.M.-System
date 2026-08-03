import { apiGet, apiPostJson } from './client.js'

/**
 * Asistencia ya registrada para un curso en una fecha dada (`YYYY-MM-DD`).
 * Se usa al iniciar una sesión de pase de lista para saber qué alumnos ya
 * tienen asistencia marcada.
 */
export function getCourseAttendanceByDate(courseId, isoDate) {
  return apiGet(`/attendance/course/${courseId}?date=${isoDate}`)
}

/**
 * Registra la asistencia de un alumno. `payload` debe respetar
 * `AttendanceSchema` (backend/app/schemas/attendance.py):
 * student_id, course_id, status, method, y opcionalmente date/time/employee_id.
 */
export function registerAttendance(payload) {
  return apiPostJson('/attendance/', payload)
}
