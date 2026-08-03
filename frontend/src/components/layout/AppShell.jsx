import { useState } from 'react'
import { ClipboardCheck, Users, UserPlus } from 'lucide-react'
import StudentEnrollment from '../enrollment/StudentEnrollment.jsx'
import AttendanceSession from '../attendance/AttendanceSession.jsx'
import StudentManagement from '../management/StudentManagement.jsx'

const TABS = [
  { id: 'enrollment', label: 'Registro de Alumno', icon: UserPlus },
  { id: 'attendance', label: 'Pase de Lista', icon: ClipboardCheck },
  { id: 'management', label: 'Administración', icon: Users },
]

/**
 * Cascarón de la aplicación: encabezado con el logo/marca y la navegación
 * entre los módulos principales. No hay enrutador instalado (no era
 * necesario para el alcance actual): la pantalla activa se controla con un
 * simple estado local.
 */
export default function AppShell() {
  const [activeTab, setActiveTab] = useState('enrollment')

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-100 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-10">
          <div className="flex items-center gap-3">
            <img src="/logo.svg" alt="B.A.M. System" className="h-10 w-10" />
            <span className="font-roboto text-lg font-bold text-moss">B.A.M. System</span>
          </div>

          <nav className="flex gap-2">
            {TABS.map((tab) => {
              const Icon = tab.icon
              const isActive = tab.id === activeTab
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setActiveTab(tab.id)}
                  className={`inline-flex items-center gap-2 rounded-lg px-4 py-2 font-roboto text-sm font-medium
                    transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/30
                    ${isActive ? 'bg-primary text-white' : 'text-moss hover:bg-mint'}`}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {tab.label}
                </button>
              )
            })}
          </nav>
        </div>
      </header>

      <main>
        {activeTab === 'enrollment' && <StudentEnrollment />}
        {activeTab === 'attendance' && <AttendanceSession />}
        {activeTab === 'management' && <StudentManagement />}
      </main>
    </div>
  )
}
