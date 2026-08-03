import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  BookOpen,
  Building2,
  Cake,
  Camera as CameraIcon,
  Check,
  Home,
  Loader2,
  Mail,
  MapPin,
  Phone,
  Save,
  ScanFace,
  ToggleLeft,
  User,
  UserRound,
} from 'lucide-react'
import Modal from '../ui/Modal.jsx'
import TextInput from '../ui/TextInput.jsx'
import SelectInput from '../ui/SelectInput.jsx'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'
import WebcamCapture from '../enrollment/WebcamCapture.jsx'
import QualityChecklist from '../enrollment/QualityChecklist.jsx'
import { getStudentById, updateStudent } from '../../api/students.js'
import { getParentById, updateParent } from '../../api/parents.js'
import { enrollStudentInCourse, unenrollStudentFromCourse } from '../../api/enrollments.js'
import { deleteBiometrics, enrollBiometrics } from '../../api/biometrics.js'
import { validateStudentData, validateTutorData } from '../../lib/validation.js'

const CHECK_ORDER = ['face', 'lighting', 'sharpness', 'centered']
const IDLE_CHECKS = { face: 'idle', lighting: 'idle', sharpness: 'idle', centered: 'idle' }

const STATUS_OPTIONS = [
  { value: 'Activo', label: 'Activo' },
  { value: 'Inactivo', label: 'Inactivo' },
]

const TABS = [
  { id: 'student', label: 'Datos del Alumno', icon: User },
  { id: 'tutor', label: 'Datos del Tutor', icon: UserRound },
  { id: 'face', label: 'Actualización de Rostro', icon: ScanFace },
]

const INITIAL_STUDENT_FORM = { name: '', lastname: '', surename: '', date_of_birth: '', status: 'Activo' }
const INITIAL_TUTOR_FORM = {
  name: '',
  lastname: '',
  surename: '',
  email: '',
  phone: '',
  dir_street: '',
  dir_col: '',
  dir_num: '',
}

/**
 * Modal de edición completa de un alumno, organizado en tres pestañas:
 * 1) Datos del alumno + asignación múltiple de cursos,
 * 2) Datos del tutor,
 * 3) Recaptura biométrica (cámara solo al abrir esta pestaña).
 */
export default function StudentEditModal({ studentId, courses, onClose, onSaved }) {
  const [activeTab, setActiveTab] = useState('student')
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(null)

  const [matricula, setMatricula] = useState('')
  const [parentId, setParentId] = useState(null)
  const [studentForm, setStudentForm] = useState(INITIAL_STUDENT_FORM)
  const [tutorForm, setTutorForm] = useState(INITIAL_TUTOR_FORM)
  const [courseIds, setCourseIds] = useState([])
  const [initialCourseIds, setInitialCourseIds] = useState([])

  const [attempted, setAttempted] = useState(false)

  const [cameraOn, setCameraOn] = useState(false)
  const [capturedImage, setCapturedImage] = useState(null)
  const [checks, setChecks] = useState(IDLE_CHECKS)
  const webcamRef = useRef(null)

  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState(null)
  const [saveWarning, setSaveWarning] = useState(null)

  useEffect(() => {
    let isActive = true
    setLoading(true)
    setLoadError(null)
    setActiveTab('student')
    setCameraOn(false)
    setCapturedImage(null)
    setChecks(IDLE_CHECKS)

    getStudentById(studentId)
      .then(async (student) => {
        if (!isActive) return

        setMatricula(student.id_student ?? '')
        setStudentForm({
          name: student.name ?? '',
          lastname: student.lastname ?? '',
          surename: student.surename ?? '',
          date_of_birth: student.date_of_birth ?? '',
          status: student.status ?? 'Activo',
        })
        setParentId(student.id_parent ?? null)

        const enrolledIds = (student.courses ?? []).map((course) => String(course.id))
        setCourseIds(enrolledIds)
        setInitialCourseIds(enrolledIds)

        if (student.id_parent) {
          const parent = await getParentById(student.id_parent)
          if (!isActive) return
          setTutorForm({
            name: parent.name ?? '',
            lastname: parent.lastname ?? '',
            surename: parent.surename ?? '',
            email: parent.email ?? '',
            phone: parent.phone ?? '',
            dir_street: parent.dir_street ?? '',
            dir_col: parent.dir_col ?? '',
            dir_num: parent.dir_num ?? '',
          })
        }
      })
      .catch((err) => {
        if (isActive) setLoadError(err.message)
      })
      .finally(() => {
        if (isActive) setLoading(false)
      })

    return () => {
      isActive = false
    }
  }, [studentId])

  // Simula la validación de calidad en tiempo real; solo corre mientras la
  // pestaña de rostro está activa y la cámara está encendida.
  useEffect(() => {
    if (activeTab !== 'face' || !cameraOn || capturedImage) {
      return undefined
    }

    setChecks(CHECK_ORDER.reduce((acc, key) => ({ ...acc, [key]: 'checking' }), {}))

    const timers = CHECK_ORDER.map((key, index) =>
      setTimeout(
        () => setChecks((prev) => ({ ...prev, [key]: 'success' })),
        700 + index * 550,
      ),
    )

    return () => timers.forEach(clearTimeout)
  }, [activeTab, cameraOn, capturedImage])

  const allChecksPassed = CHECK_ORDER.every((key) => checks[key] === 'success')

  const studentErrors = useMemo(() => validateStudentData(studentForm), [studentForm])
  const tutorErrors = useMemo(
    () => validateTutorData(tutorForm, { requirePassword: false }),
    [tutorForm],
  )
  const isValid = Object.keys(studentErrors).length === 0 && Object.keys(tutorErrors).length === 0

  const handleStudentFieldChange = useCallback((field, value) => {
    setStudentForm((prev) => ({ ...prev, [field]: value }))
  }, [])

  const handleTutorFieldChange = useCallback((field, value) => {
    setTutorForm((prev) => ({ ...prev, [field]: value }))
  }, [])

  const handleToggleCourse = useCallback((courseId) => {
    const id = String(courseId)
    setCourseIds((prev) => (prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]))
  }, [])

  const handleTabChange = useCallback((tabId) => {
    setActiveTab(tabId)
    // Apaga la cámara al salir de la pestaña de rostro para no dejar el
    // stream abierto mientras el usuario edita otros datos.
    if (tabId !== 'face') {
      setCameraOn(false)
      setChecks(IDLE_CHECKS)
    }
  }, [])

  const handleCapture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot()
    if (imageSrc) {
      setCapturedImage(imageSrc)
    }
  }, [])

  const handleRetake = useCallback(() => setCapturedImage(null), [])

  const syncCourseEnrollments = useCallback(async () => {
    const selected = new Set(courseIds)
    const initial = new Set(initialCourseIds)
    const toEnroll = [...selected].filter((id) => !initial.has(id))
    const toUnenroll = [...initial].filter((id) => !selected.has(id))
    const failures = []

    for (const id of toUnenroll) {
      try {
        await unenrollStudentFromCourse(studentId, Number(id))
      } catch (err) {
        failures.push(`baja del curso ${id}: ${err.message}`)
      }
    }

    for (const id of toEnroll) {
      try {
        await enrollStudentInCourse(studentId, Number(id))
      } catch (err) {
        failures.push(`alta del curso ${id}: ${err.message}`)
      }
    }

    return failures
  }, [courseIds, initialCourseIds, studentId])

  const handleSave = useCallback(async () => {
    setAttempted(true)
    setSaveError(null)
    setSaveWarning(null)

    if (!isValid) {
      if (Object.keys(studentErrors).length > 0) {
        setActiveTab('student')
      } else if (Object.keys(tutorErrors).length > 0) {
        setActiveTab('tutor')
      }
      return
    }

    setSaving(true)

    try {
      await updateStudent(studentId, {
        name: studentForm.name.trim(),
        lastname: studentForm.lastname.trim(),
        surename: studentForm.surename.trim() || null,
        date_of_birth: studentForm.date_of_birth,
        status: studentForm.status,
      })
    } catch (err) {
      setSaveError({ stage: 'student', message: err.message })
      setActiveTab('student')
      setSaving(false)
      return
    }

    if (parentId) {
      const tutorPayload = {
        name: tutorForm.name.trim(),
        lastname: tutorForm.lastname.trim(),
        email: tutorForm.email.trim(),
        phone: tutorForm.phone.trim(),
        dir_street: tutorForm.dir_street.trim(),
        dir_col: tutorForm.dir_col.trim(),
        dir_num: tutorForm.dir_num.trim(),
      }
      if (tutorForm.surename.trim()) {
        tutorPayload.surename = tutorForm.surename.trim()
      }

      try {
        await updateParent(parentId, tutorPayload)
      } catch (err) {
        setSaveError({ stage: 'tutor', message: err.message })
        setActiveTab('tutor')
        setSaving(false)
        return
      }
    }

    const warnings = []
    const enrollmentFailures = await syncCourseEnrollments()
    if (enrollmentFailures.length > 0) {
      warnings.push(`No se pudieron sincronizar todas las inscripciones (${enrollmentFailures.join('; ')}).`)
    }

    if (capturedImage) {
      try {
        await deleteBiometrics(studentId).catch(() => {})
        await enrollBiometrics(studentId, capturedImage)
      } catch (err) {
        warnings.push(`No se pudo actualizar el rostro enrolado: ${err.message}`)
      }
    }

    setSaving(false)

    if (warnings.length > 0) {
      setSaveWarning(`Los datos generales se guardaron, pero: ${warnings.join(' ')}`)
    }

    onSaved()
  }, [
    isValid,
    studentErrors,
    tutorErrors,
    studentId,
    studentForm,
    parentId,
    tutorForm,
    syncCourseEnrollments,
    capturedImage,
    onSaved,
  ])

  return (
    <Modal
      title={matricula ? `Editar alumno — ${matricula}` : 'Editar alumno'}
      onClose={onClose}
      maxWidthClassName="max-w-4xl"
    >
      {loading && (
        <div className="flex items-center justify-center gap-2 py-16 text-gray-400">
          <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
          <span className="font-lato text-sm">Cargando expediente...</span>
        </div>
      )}

      {!loading && loadError && (
        <Alert variant="error" title="No se pudo cargar el expediente del alumno">
          {loadError}
        </Alert>
      )}

      {!loading && !loadError && (
        <div className="flex flex-col gap-6">
          <nav
            className="flex flex-wrap gap-2 border-b border-gray-100 pb-4"
            aria-label="Secciones del expediente"
          >
            {TABS.map((tab) => {
              const Icon = tab.icon
              const isActive = tab.id === activeTab
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => handleTabChange(tab.id)}
                  className={`inline-flex items-center gap-2 rounded-lg px-4 py-2 font-roboto text-sm font-medium
                    transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/30
                    ${isActive ? 'bg-primary text-white' : 'text-moss hover:bg-mint'}`}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {tab.label}
                  {tab.id === 'face' && capturedImage && (
                    <span className="ml-1 rounded-full bg-white/20 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide">
                      Nueva
                    </span>
                  )}
                </button>
              )
            })}
          </nav>

          {activeTab === 'student' && (
            <section className="flex flex-col gap-6">
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
                <TextInput
                  label="Nombre(s)"
                  icon={User}
                  value={studentForm.name}
                  onChange={(e) => handleStudentFieldChange('name', e.target.value)}
                  error={attempted ? studentErrors.name : undefined}
                  required
                />
                <TextInput
                  label="Apellido paterno"
                  icon={User}
                  value={studentForm.lastname}
                  onChange={(e) => handleStudentFieldChange('lastname', e.target.value)}
                  error={attempted ? studentErrors.lastname : undefined}
                  required
                />
                <TextInput
                  label="Apellido materno"
                  icon={User}
                  hint="Opcional"
                  value={studentForm.surename}
                  onChange={(e) => handleStudentFieldChange('surename', e.target.value)}
                />
                <TextInput
                  label="Fecha de nacimiento"
                  icon={Cake}
                  type="date"
                  value={studentForm.date_of_birth}
                  onChange={(e) => handleStudentFieldChange('date_of_birth', e.target.value)}
                  error={attempted ? studentErrors.date_of_birth : undefined}
                  required
                />
                <SelectInput
                  label="Estatus"
                  icon={ToggleLeft}
                  value={studentForm.status}
                  onChange={(e) => handleStudentFieldChange('status', e.target.value)}
                  options={STATUS_OPTIONS}
                />
              </div>

              <div>
                <div className="mb-3 flex items-center gap-2">
                  <BookOpen className="h-4 w-4 text-primary" aria-hidden="true" />
                  <h3 className="font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
                    Cursos asignados
                  </h3>
                </div>
                <p className="mb-3 font-lato text-sm text-gray-500">
                  Selecciona uno o varios cursos. Al guardar se sincronizan altas y bajas.
                </p>

                {courses.length === 0 ? (
                  <p className="rounded-lg border border-dashed border-gray-200 bg-gray-50 px-4 py-6 text-center font-lato text-sm text-gray-400">
                    No hay cursos disponibles para asignar.
                  </p>
                ) : (
                  <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                    {courses.map((course) => {
                      const id = String(course.id)
                      const selected = courseIds.includes(id)
                      return (
                        <li key={id}>
                          <label
                            className={`flex cursor-pointer items-start gap-3 rounded-lg border px-4 py-3 transition-colors
                              ${selected ? 'border-primary bg-mint' : 'border-gray-200 bg-white hover:border-primaryLight'}`}
                          >
                            <span
                              className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded border
                                ${selected ? 'border-primary bg-primary text-white' : 'border-gray-300 bg-white'}`}
                              aria-hidden="true"
                            >
                              {selected && <Check className="h-3.5 w-3.5" />}
                            </span>
                            <input
                              type="checkbox"
                              className="sr-only"
                              checked={selected}
                              onChange={() => handleToggleCourse(id)}
                            />
                            <span className="font-lato text-sm text-moss">{course.name}</span>
                          </label>
                        </li>
                      )
                    })}
                  </ul>
                )}

                {courseIds.length > 0 && (
                  <p className="mt-3 font-lato text-xs text-gray-400">
                    {courseIds.length} curso{courseIds.length === 1 ? '' : 's'} seleccionado
                    {courseIds.length === 1 ? '' : 's'}.
                  </p>
                )}
              </div>
            </section>
          )}

          {activeTab === 'tutor' && (
            <section>
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
                <TextInput
                  label="Nombre(s)"
                  icon={User}
                  value={tutorForm.name}
                  onChange={(e) => handleTutorFieldChange('name', e.target.value)}
                  error={attempted ? tutorErrors.name : undefined}
                  required
                />
                <TextInput
                  label="Apellidos"
                  icon={User}
                  value={tutorForm.lastname}
                  onChange={(e) => handleTutorFieldChange('lastname', e.target.value)}
                  error={attempted ? tutorErrors.lastname : undefined}
                  required
                />
                <TextInput
                  label="Correo electrónico"
                  icon={Mail}
                  type="email"
                  value={tutorForm.email}
                  onChange={(e) => handleTutorFieldChange('email', e.target.value)}
                  error={attempted ? tutorErrors.email : undefined}
                  required
                />
                <TextInput
                  label="Teléfono"
                  icon={Phone}
                  type="tel"
                  value={tutorForm.phone}
                  onChange={(e) => handleTutorFieldChange('phone', e.target.value)}
                  error={attempted ? tutorErrors.phone : undefined}
                  required
                />
                <TextInput
                  label="Calle"
                  icon={MapPin}
                  value={tutorForm.dir_street}
                  onChange={(e) => handleTutorFieldChange('dir_street', e.target.value)}
                  error={attempted ? tutorErrors.dir_street : undefined}
                  required
                />
                <TextInput
                  label="Colonia"
                  icon={Building2}
                  value={tutorForm.dir_col}
                  onChange={(e) => handleTutorFieldChange('dir_col', e.target.value)}
                  error={attempted ? tutorErrors.dir_col : undefined}
                  required
                />
                <TextInput
                  label="Número"
                  icon={Home}
                  value={tutorForm.dir_num}
                  onChange={(e) => handleTutorFieldChange('dir_num', e.target.value)}
                  error={attempted ? tutorErrors.dir_num : undefined}
                  required
                />
              </div>
            </section>
          )}

          {activeTab === 'face' && (
            <section>
              <p className="mb-4 font-lato text-sm text-gray-500">
                Solo captura una nueva foto si necesitas remplazar el rostro enrolado; si no
                enciendes la cámara, se conserva el actual.
              </p>
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
                <div className="lg:col-span-3">
                  <WebcamCapture
                    ref={webcamRef}
                    cameraOn={cameraOn}
                    onEnableCamera={() => setCameraOn(true)}
                    capturedImage={capturedImage}
                    onRetake={handleRetake}
                    allChecksPassed={allChecksPassed}
                  />
                </div>
                <div className="flex flex-col gap-4 lg:col-span-2">
                  <QualityChecklist checks={checks} />
                  <Button
                    variant="primary"
                    icon={CameraIcon}
                    disabled={!cameraOn || !allChecksPassed || Boolean(capturedImage)}
                    onClick={handleCapture}
                  >
                    Capturar nueva foto
                  </Button>
                  {capturedImage && (
                    <p className="flex items-center gap-1.5 font-lato text-xs text-primary">
                      <ScanFace className="h-3.5 w-3.5" aria-hidden="true" />
                      Nueva foto lista: se guardará al confirmar los cambios.
                    </p>
                  )}
                </div>
              </div>
            </section>
          )}

          {attempted && !isValid && (
            <Alert variant="error" title="Revisa los campos marcados en rojo">
              Hay datos obligatorios incompletos o inválidos en el alumno o el tutor.
            </Alert>
          )}
          {saveError && (
            <Alert variant="error" title="No se pudieron guardar los cambios">
              {saveError.message}
            </Alert>
          )}
          {saveWarning && (
            <Alert variant="warning" title="Guardado parcial">
              {saveWarning}
            </Alert>
          )}

          <div className="flex justify-end gap-3 border-t border-gray-100 pt-6">
            <Button variant="ghost" onClick={onClose} disabled={saving}>
              Cancelar
            </Button>
            <Button variant="primary" icon={Save} loading={saving} onClick={handleSave}>
              Guardar cambios
            </Button>
          </div>
        </div>
      )}
    </Modal>
  )
}
