import { ChevronDown } from 'lucide-react'

/**
 * Select con ícono izquierdo opcional, flecha (ChevronDown) y mensaje de
 * error. Mismo lenguaje visual que `TextInput`.
 */
export default function SelectInput({
  label,
  icon: Icon,
  error,
  hint,
  placeholder,
  options = [],
  className = '',
  containerClassName = '',
  ...selectProps
}) {
  return (
    <label className={`flex flex-col gap-1.5 ${containerClassName}`}>
      <span className="font-roboto text-sm font-medium text-moss">{label}</span>
      <span className="relative flex items-center">
        {Icon && <Icon className="pointer-events-none absolute left-3 h-4 w-4 text-gray-400" aria-hidden="true" />}
        <select
          className={`w-full appearance-none rounded-lg border bg-white py-2.5 pr-9 text-sm text-moss
            transition-colors focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30
            disabled:bg-gray-50 disabled:text-gray-400
            ${Icon ? 'pl-10' : 'pl-3'}
            ${error ? 'border-red-300' : 'border-gray-200'}
            ${className}`}
          {...selectProps}
        >
          {placeholder && <option value="">{placeholder}</option>}
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <ChevronDown className="pointer-events-none absolute right-3 h-4 w-4 text-gray-400" aria-hidden="true" />
      </span>
      {hint && !error && <span className="font-lato text-xs text-gray-400">{hint}</span>}
      {error && <span className="font-lato text-xs text-red-500">{error}</span>}
    </label>
  )
}
