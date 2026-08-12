import { apiGet } from './client.js'

/** Lista de empleados (solo Administrador). */
export function getAllEmployees() {
  return apiGet('/employees/')
}
