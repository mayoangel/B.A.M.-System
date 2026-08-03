import { apiDelete, apiGet, apiPostJson } from './client.js'

/**
 * Empleados/docentes asignados a un curso. Se usa para mostrar el maestro
 * titular en la pantalla de pase de lista (se toma el primero de la lista).
 */
export function getCourseTeachers(courseId) {
  return apiGet(`/employee_course/course/${courseId}`)
}

/** Asigna un docente a un curso (solo Administrador). */
export function assignTeacherToCourse(employeeId, courseId) {
  return apiPostJson('/employee_course/assign', {
    employee_id: employeeId,
    course_id: courseId,
  })
}

/** Retira a un docente de un curso (solo Administrador). */
export function unassignTeacherFromCourse(employeeId, courseId) {
  return apiDelete('/employee_course/unassign', {
    employee_id: employeeId,
    course_id: courseId,
  })
}
