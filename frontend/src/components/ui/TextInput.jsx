/**
 * Input de texto con ícono izquierdo opcional (lucide-react) y mensaje de
 * error. Estilo consistente en todos los formularios: bordes suaves, focus
 * ring en `primary`.
 */
export default function TextInput({
  label,
  icon: Icon,
  error,
  hint,
  className = '',
  containerClassName = '',
  ...inputProps
}) {
  return (
    <label className={`flex flex-col gap-1.5 ${containerClassName}`}>
      <span className="font-roboto text-sm font-medium text-moss">{label}</span>
      <span className="relative flex items-center">
        {Icon && <Icon className="pointer-events-none absolute left-3 h-4 w-4 text-gray-400" aria-hidden="true" />}
        <input
          className={`w-full rounded-lg border bg-white py-2.5 text-sm text-moss placeholder:text-gray-400
            transition-colors focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30
            disabled:bg-gray-50 disabled:text-gray-400
            ${Icon ? 'pl-10 pr-3' : 'px-3'}
            ${error ? 'border-red-300' : 'border-gray-200'}
            ${className}`}
          {...inputProps}
        />
      </span>
      {hint && !error && <span className="font-lato text-xs text-gray-400">{hint}</span>}
      {error && <span className="font-lato text-xs text-red-500">{error}</span>}
    </label>
  )
}
