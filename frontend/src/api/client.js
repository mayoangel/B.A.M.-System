/**
 * Cliente HTTP mínimo para consumir la API de Flask del backend B.A.M.
 *
 * Se usa `fetch` nativo (sin axios) envuelto en un helper que normaliza los
 * errores del backend: los endpoints devuelven `{ error, details }` tanto
 * para errores de validación de Marshmallow (400) como para errores de
 * dominio (404/409/422), y este cliente los transforma en `ApiError`.
 */
export const API_BASE_URL = 'http://localhost:5000/api/v1'

export class ApiError extends Error {
  constructor(message, { status, details } = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details ?? null
  }
}

async function parseJsonSafely(response) {
  try {
    return await response.json()
  } catch {
    return null
  }
}

/**
 * Ejecuta una petición contra la API y lanza `ApiError` si la respuesta no
 * es exitosa. `path` debe iniciar con "/" (ej. "/students/").
 */
export async function apiRequest(path, options = {}) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, options)
  } catch {
    throw new ApiError(
      'No se pudo conectar con el servidor. Verifica que el backend esté corriendo en ' +
        `${API_BASE_URL}.`,
    )
  }

  const body = await parseJsonSafely(response)

  if (!response.ok) {
    const message = body?.error || `El servidor respondió con un error (código ${response.status}).`
    throw new ApiError(message, { status: response.status, details: body?.details })
  }

  return body
}

export function apiGet(path) {
  return apiRequest(path, { method: 'GET' })
}

export function apiPostJson(path, payload) {
  return apiRequest(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export function apiPutJson(path, payload) {
  return apiRequest(path, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export function apiDelete(path, payload) {
  return apiRequest(path, {
    method: 'DELETE',
    ...(payload
      ? { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }
      : {}),
  })
}

export function apiPostFormData(path, formData) {
  // No se fija manualmente el header 'Content-Type': el navegador debe
  // generar el boundary de multipart/form-data automáticamente.
  return apiRequest(path, { method: 'POST', body: formData })
}
