import { apiGet } from './client.js'

/**
 * Empleados/docentes asignados a un curso. Se usa para mostrar el maestro
 * titular en la pantalla de pase de lista (se toma el primero de la lista).
 */
export function getCourseTeachers(courseId) {
  return apiGet(`/employee_course/course/${courseId}`)
}
