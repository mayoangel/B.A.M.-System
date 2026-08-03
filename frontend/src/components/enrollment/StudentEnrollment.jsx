import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { ArrowLeft, ArrowRight, Camera as CameraIcon } from 'lucide-react'
import Stepper from './Stepper.jsx'
import WebcamCapture from './WebcamCapture.jsx'
import QualityChecklist from './QualityChecklist.jsx'
import StudentDataForm from './StudentDataForm.jsx'
import TutorCourseForm from './TutorCourseForm.jsx'
import ConfirmSummary from './ConfirmSummary.jsx'
import Button from '../ui/Button.jsx'
import Alert from '../ui/Alert.jsx'
import { createParent } from '../../api/parents.js'
import { createStudent } from '../../api/students.js'
import { enrollBiometrics } from '../../api/biometrics.js'
import { enrollStudentInCourse } from '../../api/enrollments.js'
import { getActiveCourses } from '../../api/courses.js'
import { validateStudentData, validateTutorData } from '../../lib/validation.js'

const CHECK_ORDER = ['face', 'lighting', 'sharpness', 'centered']
const IDLE_CHECKS = { face: 'idle', lighting: 'idle', sharpness: 'idle', centered: 'idle' }

// El alumno es menor de edad: sin credenciales ni contacto propio. La
// matrícula (`id_student`) la genera el backend automáticamente.
const INITIAL_STUDENT_DATA = {
  name: '',
  lastname: '',
  surename: '',
  date_of_birth: '',
}

// El tutor concentra ahora las credenciales, contacto y dirección; se crea
// (o reutiliza, si el correo ya existe) en el mismo paso 3. El curso es
// opcional.
const INITIAL_TUTOR_COURSE_DATA = {
  name: '',
  lastname: '',
  surename: '',
  email: '',
  phone: '',
  password: '',
  dir_street: '',
  dir_col: '',
  dir_num: '',
  course_id: '',
}
const IDLE_SUBMISSION = { status: 'idle', error: null, warning: null }

/**
 * Pantalla de Registro de Alumno — Enrolamiento Biométrico.
 * Orquesta los 4 pasos del flujo y centraliza el estado del formulario
 * completo (foto + datos de alumno + tutor/curso) y la integración real
 * con el backend de Flask.
 *
 * Orden de envío (paso 4): 1) crear/reutilizar tutor (`POST /parents/`),
 * 2) crear al alumno con el `parent_id` obtenido (`POST /students/`),
 * 3) enrolar su biometría (`POST /biometrics/enroll`) y 4) si se eligió
 * curso, inscribirlo (`POST /enrollments/enroll`).
 */
export default function StudentEnrollment() {
  const [currentStep, setCurrentStep] = useState(1)

  // --- Paso 1: captura biométrica -----------------------------------------
  const [cameraOn, setCameraOn] = useState(false)
  const [capturedImage, setCapturedImage] = useState(null)
  const [checks, setChecks] = useState(IDLE_CHECKS)
  const webcamRef = useRef(null)

  // --- Paso 2 y 3: datos del formulario ------------------------------------
  const [studentData, setStudentData] = useState(INITIAL_STUDENT_DATA)
  const [tutorCourseData, setTutorCourseData] = useState(INITIAL_TUTOR_COURSE_DATA)
  // Solo se muestran errores de un paso después de que el usuario intentó
  // avanzar al menos una vez (evita un formulario "rojo" desde el inicio).
  const [step2Attempted, setStep2Attempted] = useState(false)
  const [step3Attempted, setStep3Attempted] = useState(false)

  // --- Cursos activos (usados en el paso 3 y mostrados en el resumen) -----
  const [courses, setCourses] = useState([])
  const [coursesLoading, setCoursesLoading] = useState(true)
  const [coursesError, setCoursesError] = useState(null)

  // --- Envío al backend (paso 4) -------------------------------------------
  const [submission, setSubmission] = useState(IDLE_SUBMISSION)
  const [createdParentId, setCreatedParentId] = useState(null)
  const [createdStudentId, setCreatedStudentId] = useState(null)

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

  // Simula la validación de calidad en tiempo real que, en producción,
  // resuelve `face_engine.py` en el backend (detección, iluminación, etc.).
  useEffect(() => {
    if (!cameraOn || capturedImage) {
      return undefined
    }

    setChecks(CHECK_ORDER.reduce((acc, key) => ({ ...acc, [key]: 'checking' }), {}))

    const timers = CHECK_ORDER.map((key, index) =>
      setTimeout(
        () => {
          setChecks((prev) => ({ ...prev, [key]: 'success' }))
        },
        700 + index * 550,
      ),
    )

    return () => timers.forEach(clearTimeout)
  }, [cameraOn, capturedImage])

  const allChecksPassed = CHECK_ORDER.every((key) => checks[key] === 'success')

  // Se recalculan en cada cambio para poder mostrar retroalimentación en vivo
  // una vez que el usuario intentó avanzar (ver `step2Attempted`/`step3Attempted`).
  const studentErrors = useMemo(() => validateStudentData(studentData), [studentData])
  const tutorErrors = useMemo(() => validateTutorData(tutorCourseData), [tutorCourseData])
  const isStep2Valid = Object.keys(studentErrors).length === 0
  const isStep3Valid = Object.keys(tutorErrors).length === 0

  const courseName = useMemo(() => {
    const course = courses.find((c) => String(c.id) === String(tutorCourseData.course_id))
    return course?.name ?? ''
  }, [courses, tutorCourseData.course_id])

  // --- Handlers: Paso 1 -----------------------------------------------------
  const handleEnableCamera = useCallback(() => setCameraOn(true), [])

  const handleCapture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot()
    if (imageSrc) {
      setCapturedImage(imageSrc)
    }
  }, [])

  const handleRetake = useCallback(() => setCapturedImage(null), [])

  // --- Handlers: navegación --------------------------------------------------
  const handleContinue = useCallback(() => setCurrentStep((step) => Math.min(step + 1, 4)), [])
  const handleBack = useCallback(() => setCurrentStep((step) => Math.max(step - 1, 1)), [])

  // A diferencia de `handleContinue`, estos handlers nunca quedan "sin hacer
  // nada": si el paso no es válido, marcan el intento (lo que revela los
  // errores de cada campo y un resumen) en vez de dejar el botón deshabilitado
  // sin explicación.
  const handleContinueStep2 = useCallback(() => {
    setStep2Attempted(true)
    if (isStep2Valid) {
      setCurrentStep(3)
    }
  }, [isStep2Valid])

  const handleContinueStep3 = useCallback(() => {
    setStep3Attempted(true)
    if (isStep3Valid) {
      setCurrentStep(4)
    }
  }, [isStep3Valid])

  const handleEditTutor = useCallback(() => {
    setSubmission(IDLE_SUBMISSION)
    setCurrentStep(3)
  }, [])

  const handleEditStudent = useCallback(() => {
    setSubmission(IDLE_SUBMISSION)
    setCurrentStep(2)
  }, [])

  const handleRetryCapture = useCallback(() => {
    setSubmission(IDLE_SUBMISSION)
    setCapturedImage(null)
    setCameraOn(false)
    setCurrentStep(1)
  }, [])

  // Al finalizar un registro exitoso, se reinicia todo el formulario para
  // capturar al siguiente alumno sin tener que recargar la página.
  const handleFinish = useCallback(() => {
    setCurrentStep(1)
    setCameraOn(false)
    setCapturedImage(null)
    setChecks(IDLE_CHECKS)
    setStudentData(INITIAL_STUDENT_DATA)
    setTutorCourseData(INITIAL_TUTOR_COURSE_DATA)
    setStep2Attempted(false)
    setStep3Attempted(false)
    setSubmission(IDLE_SUBMISSION)
    setCreatedParentId(null)
    setCreatedStudentId(null)
  }, [])

  // --- Handlers: formularios --------------------------------------------------
  const handleStudentFieldChange = useCallback((field, value) => {
    setStudentData((prev) => ({ ...prev, [field]: value }))
  }, [])

  const handleTutorCourseFieldChange = useCallback((field, value) => {
    setTutorCourseData((prev) => ({ ...prev, [field]: value }))
  }, [])

  // --- Envío final: crea/reutiliza al tutor, crea al alumno, enrola su ------
  // biometría e inscribe su curso (si se seleccionó uno).
  const handleConfirm = useCallback(async () => {
    setSubmission({ status: 'submitting', error: null, warning: null })

    // Petición 1: tutor (se reutiliza si ya se creó en un intento previo).
    let parentId = createdParentId

    if (!parentId) {
      try {
        const payload = {
          name: tutorCourseData.name.trim(),
          lastname: tutorCourseData.lastname.trim(),
          email: tutorCourseData.email.trim(),
          phone: tutorCourseData.phone.trim(),
          password: tutorCourseData.password,
          dir_street: tutorCourseData.dir_street.trim(),
          dir_col: tutorCourseData.dir_col.trim(),
          dir_num: tutorCourseData.dir_num.trim(),
        }
        if (tutorCourseData.surename.trim()) {
          payload.surename = tutorCourseData.surename.trim()
        }

        const createdParent = await createParent(payload)
        parentId = createdParent.id
        setCreatedParentId(parentId)
      } catch (err) {
        setSubmission({
          status: 'error',
          error: { stage: 'parent', message: err.message, details: err.details },
          warning: null,
        })
        return
      }
    }

    // Petición 2: alumno, inyectando el `id_parent` obtenido arriba.
    let studentId = createdStudentId

    if (!studentId) {
      try {
        const payload = {
          name: studentData.name.trim(),
          lastname: studentData.lastname.trim(),
          date_of_birth: studentData.date_of_birth,
          id_parent: parentId,
        }
        if (studentData.surename.trim()) {
          payload.surename = studentData.surename.trim()
        }

        const created = await createStudent(payload)
        studentId = created.id
        setCreatedStudentId(studentId)
      } catch (err) {
        setSubmission({
          status: 'error',
          error: { stage: 'student', message: err.message, details: err.details },
          warning: null,
        })
        return
      }
    }

    // Petición 3: biometría.
    try {
      await enrollBiometrics(studentId, capturedImage)
    } catch (err) {
      setSubmission({
        status: 'error',
        error: { stage: 'biometrics', message: err.message, details: err.details },
        warning: null,
      })
      return
    }

    // Petición 4 (condicional): inscripción a curso.
    let warning = null
    if (tutorCourseData.course_id) {
      try {
        await enrollStudentInCourse(studentId, Number(tutorCourseData.course_id))
      } catch (err) {
        warning =
          'El alumno y su información biométrica se registraron correctamente, pero no se pudo ' +
          `inscribir automáticamente al curso seleccionado: ${err.message}`
      }
    }

    setSubmission({ status: 'success', error: null, warning })
  }, [createdParentId, createdStudentId, studentData, tutorCourseData, capturedImage])

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-6xl">
        <header className="mb-8">
          <h1 className="font-roboto text-2xl font-bold text-moss">Registro de Alumno</h1>
          <p className="mt-1 font-lato text-sm text-gray-500">
            Enrolamiento biométrico para el módulo de asistencia automatizada.
          </p>
        </header>

        <div className="mb-10 rounded-xl border border-gray-100 bg-white px-6 py-6 shadow-sm sm:px-10">
          <Stepper currentStep={currentStep} />
        </div>

        {currentStep === 1 && (
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
            <section className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm lg:col-span-3">
              <h2 className="mb-4 font-roboto text-base font-semibold text-moss">Captura Biométrica</h2>
              <WebcamCapture
                ref={webcamRef}
                cameraOn={cameraOn}
                onEnableCamera={handleEnableCamera}
                capturedImage={capturedImage}
                onRetake={handleRetake}
                allChecksPassed={allChecksPassed}
              />
            </section>

            <aside className="flex flex-col gap-6 rounded-xl border border-gray-100 bg-white p-6 shadow-sm lg:col-span-2">
              <div>
                <h3 className="font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
                  Instrucciones
                </h3>
                <p className="mt-2 font-lato text-sm leading-relaxed text-gray-600">
                  Pide al alumno que se coloque frente a la cámara, alineando su rostro y hombros con la
                  silueta guía, en un lugar bien iluminado. Evita lentes oscuros o gorras que cubran el
                  rostro.
                </p>
              </div>

              <div>
                <h3 className="mb-3 font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
                  Validación de calidad
                </h3>
                <QualityChecklist checks={checks} />
              </div>

              <div className="mt-auto flex flex-col gap-3 pt-2">
                <Button
                  variant="primary"
                  icon={CameraIcon}
                  onClick={handleCapture}
                  disabled={!cameraOn || Boolean(capturedImage) || !allChecksPassed}
                  className="w-full"
                >
                  Capturar Foto
                </Button>
                <Button
                  variant="secondary"
                  icon={ArrowRight}
                  iconPosition="right"
                  onClick={handleContinue}
                  disabled={!capturedImage}
                  className="w-full"
                >
                  Continuar
                </Button>
              </div>
            </aside>
          </div>
        )}

        {currentStep === 2 && (
          <section className="flex flex-col gap-6 rounded-xl border border-gray-100 bg-white p-6 shadow-sm sm:p-8">
            <h2 className="font-roboto text-base font-semibold text-moss">Datos del Alumno</h2>
            <StudentDataForm
              data={studentData}
              onChange={handleStudentFieldChange}
              errors={step2Attempted ? studentErrors : {}}
            />
            {step2Attempted && !isStep2Valid && (
              <Alert variant="error" title="Faltan datos por completar">
                Revisa los campos marcados en rojo antes de continuar.
              </Alert>
            )}
            <div className="flex justify-between border-t border-gray-100 pt-6">
              <Button variant="ghost" icon={ArrowLeft} onClick={handleBack}>
                Volver
              </Button>
              <Button variant="primary" icon={ArrowRight} iconPosition="right" onClick={handleContinueStep2}>
                Continuar
              </Button>
            </div>
          </section>
        )}

        {currentStep === 3 && (
          <section className="flex flex-col gap-6 rounded-xl border border-gray-100 bg-white p-6 shadow-sm sm:p-8">
            <h2 className="font-roboto text-base font-semibold text-moss">Tutor y Curso</h2>
            <TutorCourseForm
              data={tutorCourseData}
              onChange={handleTutorCourseFieldChange}
              errors={step3Attempted ? tutorErrors : {}}
              courses={courses}
              coursesLoading={coursesLoading}
              coursesError={coursesError}
            />
            {step3Attempted && !isStep3Valid && (
              <Alert variant="error" title="Faltan datos por completar">
                Revisa los campos marcados en rojo antes de continuar. Todos los campos del tutor son
                obligatorios, excepto el curso.
              </Alert>
            )}
            <div className="flex justify-between border-t border-gray-100 pt-6">
              <Button variant="ghost" icon={ArrowLeft} onClick={handleBack}>
                Volver
              </Button>
              <Button variant="primary" icon={ArrowRight} iconPosition="right" onClick={handleContinueStep3}>
                Continuar
              </Button>
            </div>
          </section>
        )}

        {currentStep === 4 && (
          <div className="flex flex-col gap-6">
            <ConfirmSummary
              capturedImage={capturedImage}
              studentData={studentData}
              tutorCourseData={tutorCourseData}
              courseName={courseName}
              submission={submission}
              onConfirm={handleConfirm}
              onEditTutor={handleEditTutor}
              onEditStudent={handleEditStudent}
              onRetryCapture={handleRetryCapture}
              onFinish={handleFinish}
            />
            {submission.status !== 'success' && (
              <div>
                <Button
                  variant="ghost"
                  icon={ArrowLeft}
                  onClick={handleBack}
                  disabled={submission.status === 'submitting'}
                >
                  Volver
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
