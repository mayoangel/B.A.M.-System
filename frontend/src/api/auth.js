import { apiPostJson } from './client.js'

/** POST /auth/login: login unificado (Empleados y Tutores). */
export function login(email, password) {
  return apiPostJson('/auth/login', { email, password })
}
