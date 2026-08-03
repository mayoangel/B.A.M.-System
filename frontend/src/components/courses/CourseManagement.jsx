import { useCallback, useEffect, useMemo, useState } from 'react'
import { BookOpen, Eye, Loader2, Plus, Power, PowerOff, Search } from 'lucide-react'
import TextInput from '../ui/TextInput.jsx'
import SelectInput from '../ui/SelectInput.jsx'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'
import Modal from '../ui/Modal.jsx'
import CreateCourseModal from './CreateCourseModal.jsx'
import CourseDetailModal from './CourseDetailModal.jsx'
import { activateCourse, deactivateCourse, getAllCourses } from '../../api/courses.js'
import { getAllEmployees } from '../../api/employees.js'
import { getCourseTeachers } from '../../api/employeeCourse.js'
import { getStudentsByCourse } from '../../api/students.js'
import { ApiError } from '../../api/client.js'

const STATUS_OPTIONS = [
  { value: 'Activo', label: 'Activo' },
  { value: 'Inactivo', label: 'Inactivo' },
]

const FEEDBACK_TIMEOUT_MS = 4500

function formatDate(value) {
  if (!value) return '—'
  const iso = String(value).slice(0, 10)
  try {
    return new Intl.DateTimeFormat('es-MX', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(new Date(`${iso}T00:00:00`))
  } catch {
    return iso
  }
}

/**
 * Administración de cursos (solo Administrador): listado, alta de cursos,
 * asignación de maestros y consulta de alumnos inscritos.
 */
export default function CourseManagement() {
  const [courses, setCourses] = useState([])
  const [employees, setEmployees] = useState([])
  const [courseStats, setCourseStats] = useState({})
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(null)

  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('')

  const [showCreate, setShowCreate] = useState(false)
  const [selectedCourse, setSelectedCourse] = useState(null)
  const [statusTarget, setStatusTarget] = useState(null)
  const [isUpdatingStatus, setIsUpdatingStatus] = useState(false)
  const [statusError, setStatusError] = useState(null)
  const [feedback, setFeedback] = useState(null)

  const loadStatsForCourses = useCallback(async (courseList) => {
    const entries = await Promise.all(
      courseList.map(async (course) => {
        try {
          const [teachers, students] = await Promise.all([
            getCourseTeachers(course.id),
            getStudentsByCourse(course.id),
          ])
          return [
            course.id,
            {
              teachers: Array.isArray(teachers) ? teachers.length : 0,
              students: Array.isArray(students) ? students.length : 0,
            },
          ]
        } catch {
          return [course.id, { teachers: 0, students: 0 }]
        }
      }),
    )
    return Object.fromEntries(entries)
  }, [])

  const loadData = useCallback(() => {
    setLoading(true)
    setLoadError(null)
    return Promise.all([getAllCourses(), getAllEmployees()])
      .then(async ([courseList, employeeList]) => {
        const coursesSafe = Array.isArray(courseList) ? courseList : []
        setCourses(coursesSafe)
        setEmployees(Array.isArray(employeeList) ? employeeList : [])
        const stats = await loadStatsForCourses(coursesSafe)
        setCourseStats(stats)
      })
      .catch((err) => setLoadError(err.message))
      .finally(() => setLoading(false))
  }, [loadStatsForCourses])

  useEffect(() => {
    loadData()
  }, [loadData])

  useEffect(() => {
    if (!feedback) return undefined
    const timer = setTimeout(() => setFeedback(null), FEEDBACK_TIMEOUT_MS)
    return () => clearTimeout(timer)
  }, [feedback])

  const filteredCourses = useMemo(() => {
    const term = searchTerm.trim().toLowerCase()
    return courses.filter((course) => {
      if (statusFilter && course.status !== statusFilter) return false
      if (!term) return true
      const haystack = `${course.name} ${course.category} ${course.description}`.toLowerCase()
      return haystack.includes(term)
    })
  }, [courses, searchTerm, statusFilter])

  async function handleStatusChange() {
    if (!statusTarget) return
    setIsUpdatingStatus(true)
    setStatusError(null)
    const willDeactivate = statusTarget.status === 'Activo'
    try {
      if (willDeactivate) {
        await deactivateCourse(statusTarget.id)
        setFeedback({ type: 'success', message: `Curso "${statusTarget.name}" desactivado.` })
      } else {
        await activateCourse(statusTarget.id)
        setFeedback({ type: 'success', message: `Curso "${statusTarget.name}" reactivado.` })
      }
      setStatusTarget(null)
      await loadData()
    } catch (err) {
      setStatusError(
        err instanceof ApiError
          ? err.message
          : willDeactivate
            ? 'No se pudo desactivar el curso.'
            : 'No se pudo reactivar el curso.',
      )
    } finally {
      setIsUpdatingStatus(false)
    }
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-10">
      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <BookOpen className="h-6 w-6 text-primary" aria-hidden="true" />
          <div>
            <h1 className="font-roboto text-xl font-bold text-moss">Cursos</h1>
            <p className="font-lato text-sm text-gray-500">
              Alta de cursos, asignación de maestros y consulta de alumnos inscritos.
            </p>
          </div>
        </div>
        <Button variant="primary" icon={Plus} onClick={() => setShowCreate(true)}>
          Nuevo curso
        </Button>
      </div>

      {feedback && (
        <Alert variant={feedback.type === 'success' ? 'success' : 'info'} className="mb-4">
          <p>{feedback.message}</p>
        </Alert>
      )}

      <div className="mb-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
        <TextInput
          label="Buscar"
          icon={Search}
          placeholder="Nombre, categoría..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          containerClassName="sm:col-span-2"
        />
        <SelectInput
          label="Estatus"
          placeholder="Todos"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          options={STATUS_OPTIONS}
        />
      </div>

      {loading && (
        <div className="flex items-center justify-center gap-2 py-16 text-gray-400">
          <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
          <span className="font-lato text-sm">Cargando cursos...</span>
        </div>
      )}

      {!loading && loadError && (
        <Alert variant="error" title="No se pudieron cargar los cursos">
          {loadError}
        </Alert>
      )}

      {!loading && !loadError && filteredCourses.length === 0 && (
        <div className="rounded-xl border border-gray-100 bg-white px-6 py-16 text-center shadow-sm">
          <BookOpen className="mx-auto mb-3 h-8 w-8 text-gray-300" aria-hidden="true" />
          <p className="font-lato text-sm text-gray-500">
            {courses.length === 0
              ? 'Aún no hay cursos registrados. Crea el primero con "Nuevo curso".'
              : 'Ningún curso coincide con los filtros actuales.'}
          </p>
        </div>
      )}

      {!loading && !loadError && filteredCourses.length > 0 && (
        <div className="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm">
          <table className="min-w-full divide-y divide-gray-100">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Curso
                </th>
                <th className="hidden px-4 py-3 text-left font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500 md:table-cell">
                  Periodo
                </th>
                <th className="px-4 py-3 text-left font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Maestros
                </th>
                <th className="px-4 py-3 text-left font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Alumnos
                </th>
                <th className="px-4 py-3 text-left font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Estatus
                </th>
                <th className="px-4 py-3 text-right font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredCourses.map((course) => {
                const stats = courseStats[course.id] ?? { teachers: 0, students: 0 }
                return (
                  <tr key={course.id} className="hover:bg-gray-50/80">
                    <td className="px-4 py-3">
                      <p className="font-roboto text-sm font-semibold text-moss">{course.name}</p>
                      <p className="font-lato text-xs text-gray-400">{course.category}</p>
                    </td>
                    <td className="hidden px-4 py-3 font-lato text-sm text-gray-500 md:table-cell">
                      {formatDate(course.start_date)} — {formatDate(course.end_date)}
                    </td>
                    <td className="px-4 py-3 font-lato text-sm text-gray-600">{stats.teachers}</td>
                    <td className="px-4 py-3 font-lato text-sm text-gray-600">{stats.students}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`rounded-full px-2.5 py-0.5 font-roboto text-xs font-medium ${
                          course.status === 'Activo'
                            ? 'bg-mint text-moss'
                            : 'bg-gray-100 text-gray-500'
                        }`}
                      >
                        {course.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex justify-end gap-2">
                        <Button
                          variant="ghost"
                          icon={Eye}
                          onClick={() => setSelectedCourse(course)}
                          className="!px-3"
                        >
                          Ver
                        </Button>
                        <Button
                          variant="ghost"
                          icon={course.status === 'Activo' ? PowerOff : Power}
                          onClick={() => {
                            setStatusError(null)
                            setStatusTarget(course)
                          }}
                          className={
                            course.status === 'Activo'
                              ? '!px-3 text-amber-600 hover:bg-amber-50 hover:text-amber-700'
                              : '!px-3 text-primary hover:bg-mint'
                          }
                        >
                          {course.status === 'Activo' ? 'Desactivar' : 'Reactivar'}
                        </Button>
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      {showCreate && (
        <CreateCourseModal
          onClose={() => setShowCreate(false)}
          onCreated={() => {
            setShowCreate(false)
            setFeedback({ type: 'success', message: 'Curso creado correctamente.' })
            loadData()
          }}
        />
      )}

      {selectedCourse && (
        <CourseDetailModal
          course={selectedCourse}
          employees={employees}
          onClose={() => setSelectedCourse(null)}
          onChanged={loadData}
        />
      )}

      {statusTarget && (
        <Modal
          title={statusTarget.status === 'Activo' ? 'Desactivar curso' : 'Reactivar curso'}
          onClose={() => !isUpdatingStatus && setStatusTarget(null)}
        >
          <div className="flex flex-col gap-4">
            <p className="font-lato text-sm text-gray-600">
              {statusTarget.status === 'Activo' ? (
                <>
                  ¿Confirmas desactivar el curso{' '}
                  <span className="font-roboto font-semibold text-moss">{statusTarget.name}</span>?
                  Dejará de aparecer en el pase de lista y en altas nuevas, pero se conserva el
                  historial de asistencias e inscripciones.
                </>
              ) : (
                <>
                  ¿Confirmas reactivar el curso{' '}
                  <span className="font-roboto font-semibold text-moss">{statusTarget.name}</span>?
                  Volverá a estar disponible para inscripción y pase de lista.
                </>
              )}
            </p>
            {statusError && (
              <Alert variant="error" title="No se pudo completar la acción">
                {statusError}
              </Alert>
            )}
            <div className="flex justify-end gap-3 border-t border-gray-100 pt-4">
              <Button variant="ghost" onClick={() => setStatusTarget(null)} disabled={isUpdatingStatus}>
                Cancelar
              </Button>
              <Button
                variant="primary"
                icon={statusTarget.status === 'Activo' ? PowerOff : Power}
                loading={isUpdatingStatus}
                onClick={handleStatusChange}
              >
                {statusTarget.status === 'Activo' ? 'Desactivar' : 'Reactivar'}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  )
}
