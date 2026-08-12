/** Formateadores de fecha/hora en español para la pantalla de Pase de Lista. */

const DATE_FORMATTER = new Intl.DateTimeFormat('es-MX', {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
})

const TIME_FORMATTER = new Intl.DateTimeFormat('es-MX', {
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
})

/** Ej. "Domingo, 2 de agosto de 2026". */
export function formatLongDate(date) {
  const formatted = DATE_FORMATTER.format(date)
  return formatted.charAt(0).toUpperCase() + formatted.slice(1)
}

/** Ej. "13:24:07". */
export function formatClockTime(date) {
  return TIME_FORMATTER.format(date)
}

/** Convierte un `Date` a `YYYY-MM-DD` en hora local (evita el corrimiento de `toISOString`). */
export function toIsoDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
