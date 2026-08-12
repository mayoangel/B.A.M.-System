import { apiGet, apiPostJson, apiPutJson } from './client.js'

/**
 * Crea un tutor (padre/madre). `payload` debe respetar `ParentSchema`
 * (backend/app/schemas/parents.py): name, lastname, surename?, email,
 * phone, password, dir_street, dir_col, dir_num.
 *
 * Si ya existe un tutor con el mismo correo, el backend reutiliza ese
 * registro (permite inscribir a varios hijos con el mismo tutor).
 */
export function createParent(payload) {
  return apiPostJson('/parents/', payload)
}

/** Datos completos de un tutor por su ID numérico (sin la contraseña). */
export function getParentById(parentId) {
  return apiGet(`/parents/id/${parentId}`)
}

/**
 * Actualiza los datos de un tutor (parcial) por su ID numérico. Si el
 * payload no incluye `password`, la contraseña actual no se modifica.
 */
export function updateParent(parentId, payload) {
  return apiPutJson(`/parents/id/${parentId}`, payload)
}
