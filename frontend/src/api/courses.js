import { apiGet } from './client.js'

/** Lista los cursos activos disponibles para inscripción. */
export function getActiveCourses() {
  return apiGet('/courses/active')
}

/** Lista todos los cursos (activos e inactivos); usado en filtros de administración. */
export function getAllCourses() {
  return apiGet('/courses/')
}
