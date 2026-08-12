import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { jwtDecode } from 'jwt-decode'
import { login as loginRequest } from '../api/auth.js'

// Misma llave que usa `src/api/client.js` para adjuntar el token en cada petición.
const STORAGE_KEY = 'bam_auth'

export const ROLE_ADMIN = 'admin'
export const ROLE_DOCENTE = 'docente'
export const ROLE_TUTOR = 'tutor'

/** Ruta principal a la que cada rol debe ser redirigido tras iniciar sesión. */
export function roleHomePath(role) {
  if (role === ROLE_ADMIN) return '/administracion'
  if (role === ROLE_DOCENTE) return '/pase-de-lista'
  if (role === ROLE_TUTOR) return '/mis-hijos'
  return '/login'
}

function readStoredSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null

    const parsed = JSON.parse(raw)
    if (!parsed?.token) return null

    const decoded = jwtDecode(parsed.token)
    if (decoded.exp && decoded.exp * 1000 <= Date.now()) {
      localStorage.removeItem(STORAGE_KEY)
      return null
    }

    return parsed
  } catch {
    localStorage.removeItem(STORAGE_KEY)
    return null
  }
}

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [session, setSession] = useState(readStoredSession)

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    setSession(null)
  }, [])

  // Si el backend responde 401 (token vencido/inválido) en cualquier
  // petición, se cierra la sesión de forma global.
  useEffect(() => {
    window.addEventListener('bam:unauthorized', logout)
    return () => window.removeEventListener('bam:unauthorized', logout)
  }, [logout])

  const login = useCallback(async (email, password) => {
    const result = await loginRequest(email, password)
    const nextSession = {
      token: result.token,
      user: { id: result.id, name: result.name, role: result.role },
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextSession))
    setSession(nextSession)
    return nextSession.user
  }, [])

  const value = useMemo(
    () => ({
      user: session?.user ?? null,
      isAuthenticated: Boolean(session?.user),
      login,
      logout,
    }),
    [session, login, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth debe usarse dentro de <AuthProvider>')
  }
  return ctx
}
