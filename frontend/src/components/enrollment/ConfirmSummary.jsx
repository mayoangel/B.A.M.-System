import { CheckCircle2, RotateCcw, SquarePen, UserCog } from 'lucide-react'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'
import { labelForField } from '../../lib/fieldLabels.js'

const STAGE_TITLES = {
  parent: 'No se pudo registrar al tutor',
  student: 'No se pudo registrar al alumno',
  biometrics: 'El alumno se registró, pero la validación biométrica falló',
  course: 'No se pudo completar la inscripción',
}

function SummaryRow({ label, value }) {
  return (
    <div className="flex items-start justify-between gap-4 border-b border-gray-100 py-2 last:border-0">
      <span className="font-roboto text-xs font-medium uppercase tracking-wide text-gray-400">{label}</span>
      <span className="font-lato text-sm text-moss">{value || '—'}</span>
    </div>
  )
}

/**
 * Paso 4: Resumen y Confirmar.
 * Muestra la foto capturada y los datos recolectados en los pasos 2 y 3,
 * y dispara el envío real al backend (ver `handleConfirm` en
 * `StudentEnrollment.jsx`).
 */
export default function ConfirmSummary({
  capturedImage,
  studentData,
  tutorCourseData,
  courseName,
  submission,
  onConfirm,
  onEditTutor,
  onEditStudent,
  onRetryCapture,
  onFinish,
}) {
  const isSubmitting = submission.status === 'submitting'
  const isSuccess = submission.status === 'success'
  const studentFullName = [studentData.name, studentData.lastname, studentData.surename]
    .filter(Boolean)
    .join(' ')
  const tutorFullName = [tutorCourseData.name, tutorCourseData.lastname, tutorCourseData.surename]
    .filter(Boolean)
    .join(' ')
  const tutorAddressLine = [tutorCourseData.dir_street, tutorCourseData.dir_num].filter(Boolean).join(' ')
  const tutorAddress = tutorAddressLine
    ? `${tutorAddressLine}, ${tutorCourseData.dir_col || ''}`.trim()
    : ''

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
      <section className="flex flex-col gap-4 rounded-xl border border-gray-100 bg-white p-6 shadow-sm lg:col-span-2">
        <h3 className="font-roboto text-sm font-semibold uppercase tracking-wide text-primary">Fotografía</h3>
        {capturedImage ? (
          <img
            src={capturedImage}
            alt="Captura biométrica del alumno"
            className="aspect-square w-full rounded-xl border border-gray-100 object-cover"
          />
        ) : (
          <div className="flex aspect-square w-full items-center justify-center rounded-xl border border-dashed border-gray-200 bg-gray-50">
            <span className="font-lato text-xs text-gray-400">Sin captura</span>
          </div>
        )}
      </section>

      <section className="flex flex-col gap-6 rounded-xl border border-gray-100 bg-white p-6 shadow-sm lg:col-span-3">
        <div>
          <h3 className="mb-2 font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
            Datos del alumno
          </h3>
          <SummaryRow label="Nombre completo" value={studentFullName} />
          <SummaryRow label="Fecha de nacimiento" value={studentData.date_of_birth} />
          <p className="mt-2 font-lato text-xs text-gray-400">
            La matrícula se genera automáticamente al confirmar el registro.
          </p>
        </div>

        <div>
          <h3 className="mb-2 font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
            Tutor
          </h3>
          <SummaryRow label="Nombre completo" value={tutorFullName} />
          <SummaryRow label="Correo" value={tutorCourseData.email} />
          <SummaryRow label="Teléfono" value={tutorCourseData.phone} />
          <SummaryRow label="Dirección" value={tutorAddress} />
        </div>

        <div>
          <h3 className="mb-2 font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
            Curso
          </h3>
          <SummaryRow label="Curso" value={courseName || 'Sin asignar por ahora'} />
        </div>

        {submission.error && (
          <Alert variant="error" title={STAGE_TITLES[submission.error.stage] ?? 'No se pudo completar el registro'}>
            <p>{submission.error.message}</p>
            {submission.error.details && (
              <ul className="mt-2 list-disc space-y-1 pl-4">
                {Object.entries(submission.error.details).map(([field, messages]) => (
                  <li key={field}>
                    <span className="font-medium">{labelForField(field)}:</span>{' '}
                    {[].concat(messages).join(' ')}
                  </li>
                ))}
              </ul>
            )}
            {submission.error.stage === 'parent' && (
              <Button variant="secondary" icon={UserCog} onClick={onEditTutor} className="mt-3">
                Editar datos del tutor
              </Button>
            )}
            {submission.error.stage === 'student' && (
              <Button variant="secondary" icon={SquarePen} onClick={onEditStudent} className="mt-3">
                Editar datos del alumno
              </Button>
            )}
            {submission.error.stage === 'biometrics' && (
              <Button variant="secondary" icon={RotateCcw} onClick={onRetryCapture} className="mt-3">
                Volver a capturar foto
              </Button>
            )}
          </Alert>
        )}

        {submission.warning && (
          <Alert variant="warning" title="Registro parcial">
            {submission.warning}
          </Alert>
        )}

        {isSuccess && (
          <Alert variant="success" title="Registro completado">
            El alumno y su información biométrica se guardaron correctamente en el sistema.
          </Alert>
        )}

        <Button
          variant="primary"
          icon={CheckCircle2}
          loading={isSubmitting}
          onClick={isSuccess ? onFinish : onConfirm}
          className="mt-auto w-full"
        >
          {isSuccess ? 'Finalizar' : 'Confirmar y Guardar'}
        </Button>
      </section>
    </div>
  )
}
