import { useEffect, useState } from 'react'
import { BookOpen, CalendarDays, GraduationCap, Loader2, Users } from 'lucide-react'
import { getAllStudentsDetailed } from '../../api/students.js'
import { getStudentAttendance } from '../../api/attendance.js'
import { ApiError } from '../../api/client.js'
import Alert from '../ui/Alert.jsx'

const STATUS_BADGE = {
  Asistencia: 'bg-mint text-moss',
  Retardo: 'bg-amber-50 text-amber-700',
  'Falta injustificada': 'bg-red-50 text-red-700',
  'Falta justificada': 'bg-gray-100 text-gray-600',
}

function formatDate(isoDate) {
  try {
    return new Intl.DateTimeFormat('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }).format(
      new Date(`${isoDate}T00:00:00`),
    )
  } catch {
    return isoDate
  }
}

function ChildCard({ child }) {
  const [attendance, setAttendance] = useState([])
  const [loadingAttendance, setLoadingAttendance] = useState(true)

  useEffect(() => {
    let isMounted = true
    setLoadingAttendance(true)
    getStudentAttendance(child.id)
      .then((records) => {
        if (isMounted) setAttendance(records)
      })
      .catch(() => {
        if (isMounted) setAttendance([])
      })
      .finally(() => {
        if (isMounted) setLoadingAttendance(false)
      })
    return () => {
      isMounted = false
    }
  }, [child.id])

  const recent = [...attendance]
    .sort((a, b) => (a.date < b.date ? 1 : -1))
    .slice(0, 5)

  return (
    <div className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="font-roboto text-lg font-semibold text-moss">
            {child.name} {child.lastname} {child.surename || ''}
          </p>
          <p className="font-lato text-sm text-gray-500">Matrícula: {child.id_student}</p>
        </div>
        <span
          className={`rounded-full px-3 py-1 font-roboto text-xs font-medium ${
            child.status === 'Activo' ? 'bg-mint text-moss' : 'bg-gray-100 text-gray-500'
          }`}
        >
          {child.status}
        </span>
      </div>

      <div className="mt-4 flex items-start gap-2">
        <GraduationCap className="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
        <div className="font-lato text-sm text-gray-600">
          {child.courses && child.courses.length > 0 ? (
            <span>{child.courses.map((c) => c.name).join(', ')}</span>
          ) : (
            <span className="text-gray-400">Sin curso asignado por el momento.</span>
          )}
        </div>
      </div>

      <div className="mt-5 border-t border-gray-100 pt-4">
        <div className="mb-3 flex items-center gap-2">
          <CalendarDays className="h-4 w-4 text-primary" aria-hidden="true" />
          <p className="font-roboto text-sm font-semibold text-moss">Asistencia reciente</p>
        </div>

        {loadingAttendance && (
          <div className="flex items-center gap-2 font-lato text-sm text-gray-400">
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            Cargando asistencia...
          </div>
        )}

        {!loadingAttendance && recent.length === 0 && (
          <p className="font-lato text-sm text-gray-400">Todavía no hay asistencia registrada.</p>
        )}

        {!loadingAttendance && recent.length > 0 && (
          <ul className="flex flex-col gap-2">
            {recent.map((record) => (
              <li
                key={record.id}
                className="flex items-center justify-between rounded-lg bg-gray-50 px-3 py-2 font-lato text-sm text-gray-700"
              >
                <span>{formatDate(record.date)}</span>
                <span
                  className={`rounded-full px-2.5 py-0.5 font-roboto text-xs font-medium ${
                    STATUS_BADGE[record.status] || 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {record.status}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

/**
 * Panel de solo lectura para Tutores: sus hijos, los cursos en los que
 * están inscritos y su asistencia reciente. El backend ya filtra por
 * `parent_id` (RBAC), así que aquí no se aplica ningún filtro adicional.
 */
export default function MyChildrenPanel() {
  const [children, setChildren] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let isMounted = true
    getAllStudentsDetailed()
      .then((data) => {
        if (isMounted) setChildren(data)
      })
      .catch((err) => {
        if (isMounted) {
          setError(err instanceof ApiError ? err.message : 'No se pudo cargar la información de tus hijos.')
        }
      })
      .finally(() => {
        if (isMounted) setLoading(false)
      })
    return () => {
      isMounted = false
    }
  }, [])

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-10">
      <div className="mb-6 flex items-center gap-3">
        <Users className="h-6 w-6 text-primary" aria-hidden="true" />
        <div>
          <h1 className="font-roboto text-xl font-bold text-moss">Mis hijos</h1>
          <p className="font-lato text-sm text-gray-500">
            Consulta los cursos y la asistencia de tus hijos registrados en B.A.M.
          </p>
        </div>
      </div>

      {error && (
        <Alert variant="error" className="mb-6">
          <p>{error}</p>
        </Alert>
      )}

      {loading && (
        <div className="flex items-center gap-2 font-lato text-sm text-gray-400">
          <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          Cargando información...
        </div>
      )}

      {!loading && !error && children.length === 0 && (
        <div className="rounded-xl border border-gray-100 bg-white p-8 text-center shadow-sm">
          <BookOpen className="mx-auto mb-3 h-8 w-8 text-gray-300" aria-hidden="true" />
          <p className="font-lato text-sm text-gray-500">
            Todavía no hay alumnos registrados bajo tu tutela.
          </p>
        </div>
      )}

      <div className="flex flex-col gap-4">
        {children.map((child) => (
          <ChildCard key={child.id} child={child} />
        ))}
      </div>
    </div>
  )
}
