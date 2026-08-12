/**
 * Cliente HTTP mínimo para consumir la API de Flask del backend B.A.M.
 *
 * Se usa `fetch` nativo (sin axios) envuelto en un helper que normaliza los
 * errores del backend: los endpoints devuelven `{ error, details }` tanto
 * para errores de validación de Marshmallow (400) como para errores de
 * dominio (404/409/422), y este cliente los transforma en `ApiError`.
 */
// En local: http://localhost:5000/api/v1
// En Vercel: la URL pública del túnel (ngrok/cloudflared) + /api/v1
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || 'http://localhost:5000/api/v1'

// Misma llave usada por `src/auth/AuthContext.jsx` para persistir la sesión.
// Vive aquí (y no se importa desde el contexto) para que este módulo pueda
// leer el token de forma síncrona sin depender del árbol de React.
const AUTH_STORAGE_KEY = 'bam_auth'

export class ApiError extends Error {
  constructor(message, { status, details } = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details ?? null
  }
}

function getStoredToken() {
  try {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw)?.token ?? null
  } catch {
    return null
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
 * es exitosa. `path` debe iniciar con "/" (ej. "/students/"). Adjunta
 * automáticamente el JWT de la sesión activa (RBAC), si existe.
 */
export async function apiRequest(path, options = {}) {
  const token = getStoredToken()
  const headers = new Headers(options.headers || {})
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers })
  } catch {
    throw new ApiError(
      'No se pudo conectar con el servidor. Verifica que el backend esté corriendo en ' +
        `${API_BASE_URL}.`,
    )
  }

  const body = await parseJsonSafely(response)

  if (response.status === 401) {
    // El token expiró o es inválido: se notifica globalmente para que
    // `AuthProvider` cierre la sesión y regrese al usuario al login.
    window.dispatchEvent(new CustomEvent('bam:unauthorized'))
  }

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
