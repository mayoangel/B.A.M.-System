import { AlignCenter, CheckCircle2, Circle, Focus, Loader2, ScanFace, SunMedium, XCircle } from 'lucide-react'

const CHECK_ITEMS = [
  { key: 'face', label: 'Detección de rostro', icon: ScanFace },
  { key: 'lighting', label: 'Iluminación', icon: SunMedium },
  { key: 'sharpness', label: 'Nitidez', icon: Focus },
  { key: 'centered', label: 'Posición centrada', icon: AlignCenter },
]

function StatusIcon({ status }) {
  switch (status) {
    case 'success':
      return <CheckCircle2 className="h-5 w-5 text-primary" aria-hidden="true" />
    case 'error':
      return <XCircle className="h-5 w-5 text-red-400" aria-hidden="true" />
    case 'checking':
      return <Loader2 className="h-5 w-5 animate-spin text-primaryLight" aria-hidden="true" />
    default:
      return <Circle className="h-5 w-5 text-gray-300" aria-hidden="true" />
  }
}

/**
 * Lista de indicadores de calidad de la captura biométrica.
 * `checks` es un objeto { face, lighting, sharpness, centered } con valores
 * 'idle' | 'checking' | 'success' | 'error'.
 */
export default function QualityChecklist({ checks }) {
  return (
    <ul className="flex flex-col gap-3">
      {CHECK_ITEMS.map(({ key, label, icon: Icon }) => {
        const status = checks[key] ?? 'idle'
        const isSuccess = status === 'success'

        return (
          <li
            key={key}
            className={`flex items-center justify-between rounded-lg border px-4 py-3 transition-colors duration-300
              ${isSuccess ? 'border-primaryLight bg-mint' : 'border-gray-100 bg-white'}`}
          >
            <div className="flex items-center gap-3">
              <Icon className={`h-4 w-4 ${isSuccess ? 'text-moss' : 'text-gray-400'}`} aria-hidden="true" />
              <span className="font-roboto text-sm text-moss">{label}</span>
            </div>
            <StatusIcon status={status} />
          </li>
        )
      })}
    </ul>
  )
}
