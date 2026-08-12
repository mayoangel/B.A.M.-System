import { Check } from 'lucide-react'

export const ENROLLMENT_STEPS = [
  { id: 1, label: 'Captura Biométrica' },
  { id: 2, label: 'Datos del Alumno' },
  { id: 3, label: 'Tutor y Curso' },
  { id: 4, label: 'Confirmar' },
]

/**
 * Indicador de progreso de 4 pasos para el flujo de registro de alumno.
 * `currentStep` es 1-indexado.
 */
export default function Stepper({ currentStep }) {
  return (
    <ol className="flex w-full items-start">
      {ENROLLMENT_STEPS.map((step, index) => {
        const isCompleted = step.id < currentStep
        const isCurrent = step.id === currentStep
        const isLast = index === ENROLLMENT_STEPS.length - 1

        return (
          <li key={step.id} className={`flex ${isLast ? '' : 'flex-1'} items-start`}>
            <div className="flex w-24 flex-col items-center gap-2 text-center sm:w-32">
              <div
                className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full border-2 font-roboto
                  text-sm font-semibold transition-colors duration-300
                  ${isCompleted ? 'border-primary bg-primary text-white' : ''}
                  ${isCurrent ? 'border-primary bg-white text-primary' : ''}
                  ${!isCompleted && !isCurrent ? 'border-gray-200 bg-white text-gray-400' : ''}`}
              >
                {isCompleted ? <Check className="h-4 w-4" aria-hidden="true" /> : step.id}
              </div>
              <span
                className={`font-roboto text-xs font-medium leading-tight
                  ${isCurrent ? 'text-moss' : ''}
                  ${isCompleted ? 'text-primary' : ''}
                  ${!isCompleted && !isCurrent ? 'text-gray-400' : ''}`}
              >
                {step.label}
              </span>
            </div>

            {!isLast && (
              <div
                className={`mt-[18px] h-0.5 flex-1 transition-colors duration-300 ${
                  isCompleted ? 'bg-primary' : 'bg-gray-200'
                }`}
              />
            )}
          </li>
        )
      })}
    </ol>
  )
}
