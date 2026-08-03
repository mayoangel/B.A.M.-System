import { useCallback, useEffect, useMemo, useState } from 'react'
import { BookOpen, Loader2, Pencil, Search, Trash2 } from 'lucide-react'
import TextInput from '../ui/TextInput.jsx'
import SelectInput from '../ui/SelectInput.jsx'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'
import StudentEditModal from './StudentEditModal.jsx'
import DeleteStudentModal from './DeleteStudentModal.jsx'
import { deleteStudent, getAllStudentsDetailed } from '../../api/students.js'
import { getAllCourses } from '../../api/courses.js'

const STATUS_OPTIONS = [
  { value: 'Activo', label: 'Activo' },
  { value: 'Inactivo', label: 'Inactivo' },
]

const FEEDBACK_TIMEOUT_MS = 4500

/**
 * Pantalla de Administración de Alumnos: tabla con búsqueda por
 * nombre/matrícula, filtros por curso y estatus, y acciones de edición
 * completa / baja (con eliminación permanente de datos biométricos) por fila.
 */
export default function StudentManagement() {
  const [students, setStudents] = useState([])
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(null)

  const [searchTerm, setSearchTerm] = useState('')
  const [courseFilter, setCourseFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')

  const [editingStudentId, setEditingStudentId] = useState(null)
  const [deletingStudent, setDeletingStudent] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const [deleteError, setDeleteError] = useState(null)

  const [feedback, setFeedback] = useState(null)

  const loadData = useCallback(() => {
    setLoading(true)
    setLoadError(null)
    return Promise.all([getAllStudentsDetailed(), getAllCourses()])
      .then(([studentList, courseList]) => {
        setStudents(Array.isArray(studentList) ? studentList : [])
        setCourses(Array.isArray(courseList) ? courseList : [])
      })
      .catch((err) => setLoadError(err.message))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  useEffect(() => {
    if (!feedback) {
      return undefined
    }
    const timer = setTimeout(() => setFeedback(null), FEEDBACK_TIMEOUT_MS)
    return () => clearTimeout(timer)
  }, [feedback])

  const filteredStudents = useMemo(() => {
    const term = searchTerm.trim().toLowerCase()

    return students.filter((student) => {
      if (term) {
        const haystack = `${student.name} ${student.lastname} ${student.surename ?? ''} ${student.id_student}`
          .toLowerCase()
        if (!haystack.includes(term)) {
          return false
        }
      }
      if (statusFilter && student.status !== statusFilter) {
        return false
      }
      if (courseFilter) {
        const belongsToCourse = (student.courses ?? []).some((c) => String(c.id) === courseFilter)
        if (!belongsToCourse) {
          return false
        }
      }
      return true
    })
  }, [students, searchTerm, statusFilter, courseFilter])

  const handleDeleteConfirm = useCallback(async () => {
    if (!deletingStudent) {
      return
    }
    setIsDeleting(true)
    setDeleteError(null)
    try {
      await deleteStudent(deletingStudent.id)
      setStudents((prev) => prev.filter((student) => student.id !== deletingStudent.id))
      setFeedback({
        type: 'success',
        text: `${deletingStudent.name} ${deletingStudent.lastname} fue dado de baja correctamente, incluyendo su información biométrica.`,
      })
      setDeletingStudent(null)
    } catch (err) {
      setDeleteError(err.message)
    } finally {
      setIsDeleting(false)
    }
  }, [deletingStudent])

  const handleSaved = useCallback(() => {
    setEditingStudentId(null)
    setFeedback({ type: 'success', text: 'Los cambios del alumno se guardaron correctamente.' })
    loadData()
  }, [loadData])

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-6xl">
        <header className="mb-8">
          <h1 className="font-roboto text-2xl font-bold text-moss">Administración de Alumnos</h1>
          <p className="mt-1 font-lato text-sm text-gray-500">
            Consulta, edita o da de baja a los alumnos registrados en el sistema.
          </p>
        </header>

        {feedback && (
          <Alert variant="success" title="Listo" className="mb-6">
            {feedback.text}
          </Alert>
        )}
        {loadError && (
          <Alert variant="error" title="No se pudo cargar la información" className="mb-6">
            {loadError}
          </Alert>
        )}

        <section className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 border-b border-gray-100 pb-6 sm:flex-row sm:items-end">
            <TextInput
              label="Buscar"
              icon={Search}
              placeholder="Nombre o matrícula..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              containerClassName="flex-1"
            />
            <SelectInput
              label="Curso"
              icon={BookOpen}
              placeholder="Todos los cursos"
              value={courseFilter}
              onChange={(e) => setCourseFilter(e.target.value)}
              options={courses.map((course) => ({ value: String(course.id), label: course.name }))}
              containerClassName="sm:w-56"
            />
            <SelectInput
              label="Estatus"
              placeholder="Todos"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              options={STATUS_OPTIONS}
              containerClassName="sm:w-40"
            />
          </div>

          {loading ? (
            <div className="flex items-center justify-center gap-2 py-16 text-gray-400">
              <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
              <span className="font-lato text-sm">Cargando alumnos...</span>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="mt-4 w-full text-left">
                <thead>
                  <tr className="font-roboto text-xs font-semibold uppercase tracking-wide text-gray-400">
                    <th className="px-3 py-3">Matrícula</th>
                    <th className="px-3 py-3">Alumno</th>
                    <th className="px-3 py-3">Tutor</th>
                    <th className="px-3 py-3">Curso(s)</th>
                    <th className="px-3 py-3">Estatus</th>
                    <th className="px-3 py-3 text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {filteredStudents.map((student) => (
                    <tr key={student.id} className="font-lato text-sm text-moss">
                      <td className="px-3 py-4 text-gray-500">{student.id_student}</td>
                      <td className="px-3 py-4 font-medium">
                        {[student.name, student.lastname, student.surename].filter(Boolean).join(' ')}
                      </td>
                      <td className="px-3 py-4 text-gray-500">
                        {student.parent ? `${student.parent.name} ${student.parent.lastname}` : 'Sin tutor'}
                      </td>
                      <td className="px-3 py-4 text-gray-500">
                        {student.courses?.length ? student.courses.map((c) => c.name).join(', ') : 'Sin asignar'}
                      </td>
                      <td className="px-3 py-4">
                        <span
                          className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium
                            ${student.status === 'Activo' ? 'bg-mint text-primary' : 'bg-gray-100 text-gray-500'}`}
                        >
                          {student.status}
                        </span>
                      </td>
                      <td className="px-3 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            icon={Pencil}
                            className="!px-3 !py-1.5 text-xs"
                            onClick={() => setEditingStudentId(student.id)}
                          >
                            Editar
                          </Button>
                          <Button
                            variant="ghost"
                            icon={Trash2}
                            className="!px-3 !py-1.5 text-xs !text-red-500 hover:!bg-red-50"
                            onClick={() => {
                              setDeletingStudent(student)
                              setDeleteError(null)
                            }}
                          >
                            Dar de baja
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}

                  {filteredStudents.length === 0 && (
                    <tr>
                      <td colSpan={6} className="px-3 py-10 text-center font-lato text-sm text-gray-400">
                        No se encontraron alumnos con los filtros seleccionados.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>

      {editingStudentId && (
        <StudentEditModal
          studentId={editingStudentId}
          courses={courses}
          onClose={() => setEditingStudentId(null)}
          onSaved={handleSaved}
        />
      )}

      {deletingStudent && (
        <DeleteStudentModal
          student={deletingStudent}
          onClose={() => setDeletingStudent(null)}
          onConfirm={handleDeleteConfirm}
          isDeleting={isDeleting}
          error={deleteError}
        />
      )}
    </div>
  )
}
