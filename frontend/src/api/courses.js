import { apiDelete, apiGet, apiPostJson, apiPutJson } from './client.js'

/** Lista los cursos activos disponibles para inscripción. */
export function getActiveCourses() {
  return apiGet('/courses/active')
}

/** Lista todos los cursos (activos e inactivos); usado en filtros de administración. */
export function getAllCourses() {
  return apiGet('/courses/')
}

/** Alta de un curso nuevo (solo Administrador). */
export function createCourse(payload) {
  return apiPostJson('/courses/', payload)
}

/** Baja lógica: desactiva el curso (status = Inactivo) por ID numérico. */
export function deactivateCourse(courseId) {
  return apiDelete(`/courses/id/${courseId}`)
}

/** Reactiva un curso previamente desactivado (por ID numérico). */
export function activateCourse(courseId) {
  return apiPutJson(`/courses/id/${courseId}/activate`, {})
}
