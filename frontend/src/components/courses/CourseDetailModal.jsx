import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  CalendarDays,
  GraduationCap,
  Loader2,
  Trash2,
  UserPlus,
  Users,
} from 'lucide-react'
import Modal from '../ui/Modal.jsx'
import SelectInput from '../ui/SelectInput.jsx'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'
import { getStudentsByCourse } from '../../api/students.js'
import {
  assignTeacherToCourse,
  getCourseTeachers,
  unassignTeacherFromCourse,
} from '../../api/employeeCourse.js'
import { ApiError } from '../../api/client.js'

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
 * Detalle de un curso: maestros asignados (alta/baja) y alumnos inscritos.
 */
export default function CourseDetailModal({ course, employees, onClose, onChanged }) {
  const [teachers, setTeachers] = useState([])
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(null)

  const [selectedTeacherId, setSelectedTeacherId] = useState('')
  const [assigning, setAssigning] = useState(false)
  const [removingId, setRemovingId] = useState(null)
  const [actionError, setActionError] = useState(null)

  const loadDetail = useCallback(() => {
    setLoading(true)
    setLoadError(null)
    return Promise.all([getCourseTeachers(course.id), getStudentsByCourse(course.id)])
      .then(([teacherList, studentList]) => {
        setTeachers(Array.isArray(teacherList) ? teacherList : [])
        setStudents(Array.isArray(studentList) ? studentList : [])
      })
      .catch((err) => setLoadError(err.message))
      .finally(() => setLoading(false))
  }, [course.id])

  useEffect(() => {
    loadDetail()
  }, [loadDetail])

  const availableTeachers = useMemo(() => {
    const assignedIds = new Set(teachers.map((t) => t.id))
    return (employees ?? [])
      .filter(
        (emp) =>
          emp.status === 'Activo' &&
          emp.role_id !== 1 &&
          !assignedIds.has(emp.id),
      )
      .map((emp) => ({
        value: String(emp.id),
        label: `${emp.name} ${emp.lastname}`,
      }))
  }, [employees, teachers])

  async function handleAssign() {
    if (!selectedTeacherId) return
    setAssigning(true)
    setActionError(null)
    try {
      await assignTeacherToCourse(Number(selectedTeacherId), course.id)
      setSelectedTeacherId('')
      await loadDetail()
      onChanged?.()
    } catch (err) {
      setActionError(err instanceof ApiError ? err.message : 'No se pudo asignar al docente.')
    } finally {
      setAssigning(false)
    }
  }

  async function handleUnassign(teacher) {
    setRemovingId(teacher.id)
    setActionError(null)
    try {
      await unassignTeacherFromCourse(teacher.id, course.id)
      await loadDetail()
      onChanged?.()
    } catch (err) {
      setActionError(err instanceof ApiError ? err.message : 'No se pudo retirar al docente.')
    } finally {
      setRemovingId(null)
    }
  }

  return (
    <Modal title={course.name} onClose={onClose} maxWidthClassName="max-w-3xl">
      <div className="flex flex-col gap-6">
        <section className="rounded-lg border border-gray-100 bg-gray-50 px-4 py-3">
          <p className="font-lato text-sm text-gray-600">{course.description}</p>
          <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 font-lato text-xs text-gray-500">
            <span>Categoría: {course.category}</span>
            <span className="inline-flex items-center gap-1">
              <CalendarDays className="h-3.5 w-3.5" aria-hidden="true" />
              {formatDate(course.start_date)} — {formatDate(course.end_date)}
            </span>
            <span>{course.time_duration}</span>
            <span>{course.days_of_week || 'Días no definidos'}</span>
            <span
              className={`rounded-full px-2 py-0.5 font-roboto text-xs font-medium ${
                course.status === 'Activo' ? 'bg-mint text-moss' : 'bg-gray-200 text-gray-600'
              }`}
            >
              {course.status}
            </span>
          </div>
        </section>

        {loading && (
          <div className="flex items-center justify-center gap-2 py-10 text-gray-400">
            <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
            <span className="font-lato text-sm">Cargando detalle del curso...</span>
          </div>
        )}

        {!loading && loadError && (
          <Alert variant="error" title="No se pudo cargar el detalle">
            {loadError}
          </Alert>
        )}

        {!loading && !loadError && (
          <>
            <section>
              <div className="mb-3 flex items-center gap-2">
                <GraduationCap className="h-4 w-4 text-primary" aria-hidden="true" />
                <h3 className="font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
                  Maestros asignados
                </h3>
              </div>

              <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-end">
                <SelectInput
                  label="Asignar docente"
                  icon={UserPlus}
                  placeholder="Selecciona un docente"
                  value={selectedTeacherId}
                  onChange={(e) => setSelectedTeacherId(e.target.value)}
                  options={availableTeachers}
                  containerClassName="flex-1"
                />
                <Button
                  variant="primary"
                  icon={UserPlus}
                  loading={assigning}
                  disabled={!selectedTeacherId}
                  onClick={handleAssign}
                >
                  Asignar
                </Button>
              </div>

              {teachers.length === 0 ? (
                <p className="rounded-lg border border-dashed border-gray-200 bg-gray-50 px-4 py-5 text-center font-lato text-sm text-gray-400">
                  Este curso aún no tiene maestros asignados.
                </p>
              ) : (
                <ul className="divide-y divide-gray-100 rounded-lg border border-gray-100">
                  {teachers.map((teacher) => (
                    <li
                      key={teacher.id}
                      className="flex items-center justify-between gap-3 px-4 py-3"
                    >
                      <div>
                        <p className="font-roboto text-sm font-medium text-moss">
                          {teacher.name} {teacher.lastname}
                        </p>
                        <p className="font-lato text-xs text-gray-400">{teacher.email}</p>
                      </div>
                      <Button
                        variant="ghost"
                        icon={Trash2}
                        loading={removingId === teacher.id}
                        onClick={() => handleUnassign(teacher)}
                        className="text-red-500 hover:bg-red-50 hover:text-red-600"
                      >
                        Retirar
                      </Button>
                    </li>
                  ))}
                </ul>
              )}
            </section>

            <section>
              <div className="mb-3 flex items-center gap-2">
                <Users className="h-4 w-4 text-primary" aria-hidden="true" />
                <h3 className="font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
                  Alumnos inscritos ({students.length})
                </h3>
              </div>

              {students.length === 0 ? (
                <p className="rounded-lg border border-dashed border-gray-200 bg-gray-50 px-4 py-5 text-center font-lato text-sm text-gray-400">
                  Todavía no hay alumnos inscritos en este curso.
                </p>
              ) : (
                <div className="overflow-hidden rounded-lg border border-gray-100">
                  <table className="min-w-full divide-y divide-gray-100">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500">
                          Matrícula
                        </th>
                        <th className="px-4 py-2 text-left font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500">
                          Nombre
                        </th>
                        <th className="px-4 py-2 text-left font-roboto text-xs font-semibold uppercase tracking-wide text-gray-500">
                          Estatus
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 bg-white">
                      {students.map((student) => (
                        <tr key={student.id}>
                          <td className="px-4 py-2.5 font-lato text-sm text-gray-500">
                            {student.id_student}
                          </td>
                          <td className="px-4 py-2.5 font-roboto text-sm font-medium text-moss">
                            {student.name} {student.lastname}
                          </td>
                          <td className="px-4 py-2.5">
                            <span
                              className={`rounded-full px-2 py-0.5 font-roboto text-xs font-medium ${
                                student.status === 'Activo'
                                  ? 'bg-mint text-moss'
                                  : 'bg-gray-100 text-gray-500'
                              }`}
                            >
                              {student.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>
          </>
        )}

        {actionError && (
          <Alert variant="error" title="No se pudo completar la acción">
            {actionError}
          </Alert>
        )}

        <div className="flex justify-end border-t border-gray-100 pt-5">
          <Button variant="ghost" onClick={onClose}>
            Cerrar
          </Button>
        </div>
      </div>
    </Modal>
  )
}
