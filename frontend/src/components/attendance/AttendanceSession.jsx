import { useCallback, useEffect, useMemo, useState } from 'react'
import { CalendarDays, Clock, GraduationCap, Loader2, LogOut } from 'lucide-react'
import Button from '../ui/Button.jsx'
import Alert from '../ui/Alert.jsx'
import CourseSelector from './CourseSelector.jsx'
import AttendanceRoster from './AttendanceRoster.jsx'
import AttendanceCamera from './AttendanceCamera.jsx'
import { getActiveCourses } from '../../api/courses.js'
import { getStudentsByCourse } from '../../api/students.js'
import { getCourseTeachers } from '../../api/employeeCourse.js'
import { getCourseAttendanceByDate, registerAttendance } from '../../api/attendance.js'
import { identifyFace } from '../../api/biometrics.js'
import { formatClockTime, formatLongDate, toIsoDate } from '../../lib/formatters.js'

// Cuánto tiempo se mantiene visible un mensaje de reconocimiento sobre la
// cámara antes de desvanecerse (da tiempo a leerlo sin saturar la pantalla).
const STATUS_MESSAGE_TIMEOUT_MS = 4000

/**
 * Pantalla de Pase de Lista (RF-03): se elige un curso, se carga su lista de
 * alumnos y se enciende la cámara para reconocerlos automáticamente. Cada
 * rostro identificado marca la asistencia del alumno correspondiente; también
 * se permite el registro manual como respaldo (RF-08).
 */
export default function AttendanceSession() {
  const [phase, setPhase] = useState('select') // 'select' | 'loading' | 'session'

  const [courses, setCourses] = useState([])
  const [coursesLoading, setCoursesLoading] = useState(true)
  const [coursesError, setCoursesError] = useState(null)

  const [course, setCourse] = useState(null)
  const [teacherName, setTeacherName] = useState('')
  const [roster, setRoster] = useState([])
  const [sessionError, setSessionError] = useState(null)

  const [cameraOn, setCameraOn] = useState(false)
  const [scanStatus, setScanStatus] = useState(null)
  const [manuallyMarkingId, setManuallyMarkingId] = useState(null)

  const [now, setNow] = useState(() => new Date())

  useEffect(() => {
    let isActive = true
    setCoursesLoading(true)
    getActiveCourses()
      .then((list) => {
        if (isActive) setCourses(Array.isArray(list) ? list : [])
      })
      .catch((err) => {
        if (isActive) setCoursesError(err.message)
      })
      .finally(() => {
        if (isActive) setCoursesLoading(false)
      })
    return () => {
      isActive = false
    }
  }, [])

  // Reloj en vivo, solo mientras hay una sesión activa.
  useEffect(() => {
    if (phase !== 'session') {
      return undefined
    }
    const interval = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(interval)
  }, [phase])

  // Los mensajes de reconocimiento se autolimpian para no saturar la cámara.
  useEffect(() => {
    if (!scanStatus) {
      return undefined
    }
    const timer = setTimeout(() => setScanStatus(null), STATUS_MESSAGE_TIMEOUT_MS)
    return () => clearTimeout(timer)
  }, [scanStatus])

  const handleSelectCourse = useCallback(async (selectedCourse) => {
    setPhase('loading')
    setSessionError(null)
    setCourse(selectedCourse)

    const todayIso = toIsoDate(new Date())

    try {
      const [students, teachers, todayAttendance] = await Promise.all([
        getStudentsByCourse(selectedCourse.id),
        getCourseTeachers(selectedCourse.id).catch(() => []),
        getCourseAttendanceByDate(selectedCourse.id, todayIso).catch(() => []),
      ])

      const presentIds = new Set((todayAttendance ?? []).map((record) => record.student_id))

      setRoster(
        (students ?? []).map((student) => ({
          ...student,
          status: presentIds.has(student.id) ? 'present' : 'pending',
          method: presentIds.has(student.id) ? 'Registrado' : null,
        })),
      )
      setTeacherName(
        teachers && teachers.length > 0 ? `${teachers[0].name} ${teachers[0].lastname}` : 'Sin asignar',
      )
      setNow(new Date())
      setPhase('session')
    } catch (err) {
      setSessionError(err.message)
      setPhase('select')
    }
  }, [])

  const handleEndSession = useCallback(() => {
    setPhase('select')
    setCourse(null)
    setRoster([])
    setTeacherName('')
    setCameraOn(false)
    setScanStatus(null)
    setSessionError(null)
  }, [])

  const markPresent = useCallback(
    async (student, method) => {
      await registerAttendance({
        student_id: student.id,
        course_id: course.id,
        status: 'Presente',
        method,
      })
      setRoster((prev) =>
        prev.map((item) => (item.id === student.id ? { ...item, status: 'present', method } : item)),
      )
    },
    [course],
  )

  const handleManualMark = useCallback(
    async (student) => {
      setManuallyMarkingId(student.id)
      try {
        await markPresent(student, 'Manual')
        setScanStatus({ type: 'success', text: `${student.name} ${student.lastname} marcado manualmente.` })
      } catch (err) {
        setScanStatus({ type: 'error', text: `No se pudo registrar a ${student.name}: ${err.message}` })
      } finally {
        setManuallyMarkingId(null)
      }
    },
    [markPresent],
  )

  const handleFrame = useCallback(
    async (frameDataUrl) => {
      setScanStatus({ type: 'scanning', text: 'Analizando rostro...' })
      try {
        const result = await identifyFace(frameDataUrl)
        const student = roster.find((item) => item.id === result.student_id)

        if (!student) {
          setScanStatus({ type: 'warning', text: 'Rostro reconocido, pero no pertenece a este curso.' })
          return
        }
        if (student.status === 'present') {
          setScanStatus({
            type: 'info',
            text: `${student.name} ${student.lastname} ya tiene asistencia registrada.`,
          })
          return
        }

        await markPresent(student, 'Biométrico')
        setScanStatus({ type: 'success', text: `Bienvenido, ${student.name} ${student.lastname}.` })
      } catch (err) {
        if (err.status === 422) {
          // Rostro no detectado / mala calidad / etc.: mensaje discreto, se repetirá en el siguiente escaneo.
          setScanStatus({ type: 'idle', text: err.message })
        } else if (err.status === 404) {
          setScanStatus({ type: 'warning', text: err.message })
        } else {
          setScanStatus({ type: 'error', text: err.message })
        }
      }
    },
    [roster, markPresent],
  )

  const presentCount = useMemo(() => roster.filter((student) => student.status === 'present').length, [roster])

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-6xl">
        <header className="mb-8">
          <h1 className="font-roboto text-2xl font-bold text-moss">Pase de Lista</h1>
          <p className="mt-1 font-lato text-sm text-gray-500">
            Reconocimiento facial en tiempo real para el registro automatizado de asistencia.
          </p>
        </header>

        {sessionError && (
          <Alert variant="error" title="No se pudo iniciar la sesión" className="mb-6">
            {sessionError}
          </Alert>
        )}

        {phase === 'select' && (
          <CourseSelector
            courses={courses}
            loading={coursesLoading}
            error={coursesError}
            onSelectCourse={handleSelectCourse}
          />
        )}

        {phase === 'loading' && (
          <div className="flex items-center justify-center gap-2 rounded-xl border border-gray-100 bg-white py-16 shadow-sm">
            <Loader2 className="h-5 w-5 animate-spin text-primary" aria-hidden="true" />
            <span className="font-lato text-sm text-gray-500">Preparando la sesión de pase de lista...</span>
          </div>
        )}

        {phase === 'session' && course && (
          <div className="flex flex-col gap-6">
            <section className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-gray-100 bg-white px-6 py-5 shadow-sm">
              <div>
                <p className="font-roboto text-lg font-semibold text-moss">{course.name}</p>
                <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 font-lato text-xs text-gray-500">
                  <span className="inline-flex items-center gap-1.5">
                    <GraduationCap className="h-3.5 w-3.5" aria-hidden="true" />
                    {teacherName}
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <CalendarDays className="h-3.5 w-3.5" aria-hidden="true" />
                    {formatLongDate(now)}
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <Clock className="h-3.5 w-3.5" aria-hidden="true" />
                    {formatClockTime(now)}
                  </span>
                </div>
              </div>
              <Button variant="secondary" icon={LogOut} onClick={handleEndSession}>
                Finalizar clase
              </Button>
            </section>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
              <section className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm lg:col-span-3">
                <h2 className="mb-4 font-roboto text-base font-semibold text-moss">Reconocimiento facial</h2>
                <AttendanceCamera
                  cameraOn={cameraOn}
                  onEnableCamera={() => setCameraOn(true)}
                  onFrame={handleFrame}
                  status={scanStatus}
                />
                <p className="mt-3 font-lato text-xs text-gray-400">
                  {presentCount} de {roster.length} alumnos con asistencia registrada.
                </p>
              </section>

              <div className="lg:col-span-2">
                <AttendanceRoster roster={roster} onMarkManual={handleManualMark} markingId={manuallyMarkingId} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
