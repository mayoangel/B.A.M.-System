import { apiDelete, apiPostJson } from './client.js'

/** Inscribe a un alumno ya registrado en un curso. */
export function enrollStudentInCourse(studentId, courseId) {
  return apiPostJson('/enrollments/enroll', { student_id: studentId, course_id: courseId })
}

/** Da de baja a un alumno de un curso específico (usado al cambiar de curso). */
export function unenrollStudentFromCourse(studentId, courseId) {
  return apiDelete('/enrollments/unenroll', { student_id: studentId, course_id: courseId })
}
