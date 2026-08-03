import { AlertTriangle, CheckCircle2, Info } from 'lucide-react'

const VARIANTS = {
  error: {
    container: 'border-red-100 bg-red-50/80 text-red-900',
    icon: AlertTriangle,
    iconClass: 'text-red-400',
  },
  warning: {
    container: 'border-amber-100 bg-amber-50/80 text-amber-900',
    icon: AlertTriangle,
    iconClass: 'text-amber-400',
  },
  success: {
    container: 'border-primaryLight bg-mint text-moss',
    icon: CheckCircle2,
    iconClass: 'text-primary',
  },
  info: {
    container: 'border-gray-200 bg-gray-50 text-gray-700',
    icon: Info,
    iconClass: 'text-gray-400',
  },
}

/**
 * Alerta minimalista y corporativa (sin emojis) para mensajes de éxito,
 * advertencia o error. Diseñada para no romper la estética general:
 * fondo muy tenue, borde suave y texto oscuro legible.
 */
export default function Alert({ variant = 'info', title, children, className = '' }) {
  const config = VARIANTS[variant] ?? VARIANTS.info
  const Icon = config.icon

  return (
    <div
      role={variant === 'error' ? 'alert' : 'status'}
      className={`flex gap-3 rounded-lg border px-4 py-3 ${config.container} ${className}`}
    >
      <Icon className={`mt-0.5 h-5 w-5 shrink-0 ${config.iconClass}`} aria-hidden="true" />
      <div className="flex-1 font-lato text-sm leading-relaxed">
        {title && <p className="font-roboto text-sm font-semibold">{title}</p>}
        {children}
      </div>
    </div>
  )
}
