import { Navigate, useLocation } from 'react-router-dom'
import { useAuth, roleHomePath } from '../../auth/AuthContext.jsx'

/**
 * Protege una ruta según el rol activo:
 *  - Sin sesión -> redirige a /login.
 *  - Rol no autorizado para esta ruta -> redirige a su panel correspondiente
 *    (nunca muestra el contenido de una sección que no le pertenece).
 */
export default function ProtectedRoute({ allowedRoles, children }) {
  const { isAuthenticated, user } = useAuth()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to={roleHomePath(user.role)} replace />
  }

  return children
}
