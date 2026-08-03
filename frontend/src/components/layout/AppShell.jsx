import { BookOpen, ClipboardCheck, LogOut, Users, UserPlus } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'
import { useAuth, ROLE_ADMIN, ROLE_DOCENTE } from '../../auth/AuthContext.jsx'

const NAV_ITEMS = [
  { to: '/registro-alumno', label: 'Registrar Alumno', icon: UserPlus, roles: [ROLE_ADMIN, ROLE_DOCENTE] },
  { to: '/pase-de-lista', label: 'Pase de Lista', icon: ClipboardCheck, roles: [ROLE_ADMIN, ROLE_DOCENTE] },
  { to: '/administracion', label: 'Alumnos', icon: Users, roles: [ROLE_ADMIN] },
  { to: '/cursos', label: 'Cursos', icon: BookOpen, roles: [ROLE_ADMIN] },
]

/**
 * Cascarón de la aplicación: encabezado con el logo/marca, navegación entre
 * módulos (renderizada dinámicamente según el rol activo, RBAC) y botón de
 * cerrar sesión. El contenido de cada pantalla llega vía `<Outlet />` del
 * enrutador (`react-router-dom`).
 */
export default function AppShell() {
  const { user, logout } = useAuth()
  const visibleItems = NAV_ITEMS.filter((item) => item.roles.includes(user?.role))

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-100 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-10">
          <div className="flex items-center gap-3">
            <img src="/logo.svg" alt="B.A.M. System" className="h-10 w-10" />
            <span className="font-roboto text-lg font-bold text-moss">B.A.M. System</span>
          </div>

          <nav className="flex flex-wrap items-center gap-2">
            {visibleItems.map((item) => {
              const Icon = item.icon
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `inline-flex items-center gap-2 rounded-lg px-4 py-2 font-roboto text-sm font-medium
                    transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/30
                    ${isActive ? 'bg-primary text-white' : 'text-moss hover:bg-mint'}`
                  }
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {item.label}
                </NavLink>
              )
            })}
          </nav>

          <div className="flex items-center gap-3 border-l border-gray-100 pl-4">
            <div className="text-right">
              <p className="font-roboto text-sm font-semibold text-moss">{user?.name}</p>
              <p className="font-lato text-xs capitalize text-gray-400">{user?.role}</p>
            </div>
            <button
              type="button"
              onClick={logout}
              title="Cerrar sesión"
              className="inline-flex items-center gap-2 rounded-lg px-3 py-2 font-roboto text-sm font-medium
                text-gray-500 transition-colors hover:bg-red-50 hover:text-red-600 focus:outline-none
                focus-visible:ring-2 focus-visible:ring-red-200"
            >
              <LogOut className="h-4 w-4" aria-hidden="true" />
              Cerrar sesión
            </button>
          </div>
        </div>
      </header>

      <main>
        <Outlet />
      </main>
    </div>
  )
}
