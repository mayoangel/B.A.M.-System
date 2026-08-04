import { apiGet } from './client.js'

/** Resumen del dashboard */
export function getSummary() {
  return apiGet('/dashboard/summary')
}

/** Cursos para la gráfica */
export function getCourses() {
  return apiGet('/dashboard/courses')
}

/** Asistencia semanal */
export function getWeeklyAttendance() {
  return apiGet('/dashboard/weekly-attendance')
}