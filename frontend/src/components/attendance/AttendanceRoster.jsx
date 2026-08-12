import { CheckCircle2, Circle, UserCheck } from 'lucide-react'
import Button from '../ui/Button.jsx'

/**
 * Lista de alumnos del curso activo, con su estatus de asistencia del día.
 * Incluye un botón de registro manual por alumno (RF-08: toda funcionalidad
 * biométrica debe permitir el registro manual como respaldo).
 */
export default function AttendanceRoster({ roster, onMarkManual, markingId }) {
  const presentCount = roster.filter((student) => student.status === 'present').length

  return (
    <section className="flex h-full flex-col gap-4 rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <h2 className="font-roboto text-base font-semibold text-moss">Lista de alumnos</h2>
        <span className="font-lato text-xs text-gray-400">
          {presentCount} / {roster.length} presentes
        </span>
      </div>

      <ul className="flex flex-1 flex-col divide-y divide-gray-100 overflow-y-auto">
        {roster.map((student) => {
          const isPresent = student.status === 'present'
          const isMarking = markingId === student.id

          return (
            <li key={student.id} className="flex items-center justify-between gap-3 py-3">
              <div className="flex min-w-0 items-center gap-3">
                <span
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full
                    ${isPresent ? 'bg-mint text-primary' : 'bg-gray-100 text-gray-400'}`}
                >
                  {isPresent ? (
                    <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
                  ) : (
                    <Circle className="h-4 w-4" aria-hidden="true" />
                  )}
                </span>
                <div className="min-w-0">
                  <p className="truncate font-roboto text-sm font-medium text-moss">
                    {student.name} {student.lastname}
                  </p>
                  <p className="font-lato text-xs text-gray-400">{student.id_student}</p>
                </div>
              </div>

              {isPresent ? (
                <span className="shrink-0 font-lato text-xs font-medium text-primary">
                  {student.method === 'Biométrico' ? 'Reconocido' : 'Registrado'}
                </span>
              ) : (
                <Button
                  variant="ghost"
                  icon={UserCheck}
                  loading={isMarking}
                  onClick={() => onMarkManual(student)}
                  className="!px-3 !py-1.5 shrink-0 text-xs"
                >
                  Marcar manual
                </Button>
              )}
            </li>
          )
        })}

        {roster.length === 0 && (
          <li className="py-8 text-center font-lato text-sm text-gray-400">
            Este curso no tiene alumnos inscritos.
          </li>
        )}
      </ul>
    </section>
  )
}
