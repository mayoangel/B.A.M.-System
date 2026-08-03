import { Loader2 } from 'lucide-react'

const VARIANT_CLASSES = {
  primary:
    'bg-primary text-white hover:bg-primaryDark focus-visible:ring-primary/40 disabled:bg-primaryLight disabled:text-white/70',
  secondary:
    'bg-white text-moss border border-gray-200 hover:bg-mint focus-visible:ring-primary/30 disabled:text-gray-300 disabled:border-gray-100 disabled:hover:bg-white',
  ghost:
    'bg-transparent text-moss hover:bg-mint focus-visible:ring-primary/20 disabled:text-gray-300 disabled:hover:bg-transparent',
}

/**
 * Botón base del sistema de diseño de B.A.M. Centraliza estilos (colores,
 * radios, sombras) para no repetir clases de Tailwind en cada pantalla.
 */
export default function Button({
  children,
  variant = 'primary',
  icon: Icon,
  iconPosition = 'left',
  loading = false,
  disabled = false,
  className = '',
  type = 'button',
  ...props
}) {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-5 py-2.5 font-roboto text-sm
        font-medium transition-colors duration-150 focus:outline-none focus-visible:ring-2
        focus-visible:ring-offset-2 disabled:cursor-not-allowed ${VARIANT_CLASSES[variant]} ${className}`}
      {...props}
    >
      {loading && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
      {!loading && Icon && iconPosition === 'left' && <Icon className="h-4 w-4" aria-hidden="true" />}
      {children}
      {!loading && Icon && iconPosition === 'right' && <Icon className="h-4 w-4" aria-hidden="true" />}
    </button>
  )
}
