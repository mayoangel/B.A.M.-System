/**
 * Validaciones de formulario en vivo para los pasos 2 y 3 del enrolamiento.
 * Reflejan las mismas reglas que `StudentSchema` y `ParentSchema` en el
 * backend (backend/app/schemas/), para que el usuario reciba retroalimentación
 * inmediata en el frontend en vez de descubrir el error hasta el envío final.
 */

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const PHONE_REGEX = /^\d{10}$/

export const MIN_STUDENT_AGE = 3
export const MAX_STUDENT_AGE = 99
export const TUTOR_PASSWORD_MIN_LENGTH = 8

function getAgeFromDateOfBirth(dateString) {
  const dob = new Date(`${dateString}T00:00:00`)
  if (Number.isNaN(dob.getTime())) {
    return null
  }

  const today = new Date()
  let age = today.getFullYear() - dob.getFullYear()
  const hasHadBirthdayThisYear =
    today.getMonth() > dob.getMonth() ||
    (today.getMonth() === dob.getMonth() && today.getDate() >= dob.getDate())
  if (!hasHadBirthdayThisYear) {
    age -= 1
  }

  return { age, dob, today }
}

/** Valida los datos del alumno (Paso 2). Devuelve un mapa `{ campo: mensaje }`. */
export function validateStudentData(data) {
  const errors = {}

  if (!data.name.trim()) {
    errors.name = 'El nombre es obligatorio.'
  }
  if (!data.lastname.trim()) {
    errors.lastname = 'El apellido paterno es obligatorio.'
  }

  if (!data.date_of_birth) {
    errors.date_of_birth = 'La fecha de nacimiento es obligatoria.'
  } else {
    const result = getAgeFromDateOfBirth(data.date_of_birth)
    if (!result) {
      errors.date_of_birth = 'La fecha de nacimiento no es válida.'
    } else if (result.dob > result.today) {
      errors.date_of_birth = 'La fecha de nacimiento no puede ser futura.'
    } else if (result.age < MIN_STUDENT_AGE || result.age > MAX_STUDENT_AGE) {
      errors.date_of_birth =
        `La edad del alumno debe estar entre ${MIN_STUDENT_AGE} y ${MAX_STUDENT_AGE} años.`
    }
  }

  return errors
}

/**
 * Valida los datos del tutor (Paso 3 del enrolamiento, y también el
 * formulario de edición en Administración de Alumnos). `requirePassword`
 * se desactiva en edición, donde la contraseña es opcional (si se deja
 * vacía, el backend conserva la actual).
 */
export function validateTutorData(data, { requirePassword = true } = {}) {
  const errors = {}

  if (!data.name.trim()) {
    errors.name = 'El nombre es obligatorio.'
  }
  if (!data.lastname.trim()) {
    errors.lastname = 'Los apellidos son obligatorios.'
  }

  if (!data.email.trim()) {
    errors.email = 'El correo electrónico es obligatorio.'
  } else if (!EMAIL_REGEX.test(data.email.trim())) {
    errors.email = 'Ingresa un correo electrónico válido.'
  }

  if (!data.phone.trim()) {
    errors.phone = 'El teléfono es obligatorio.'
  } else if (!PHONE_REGEX.test(data.phone.trim())) {
    errors.phone = 'El teléfono debe tener 10 dígitos, sin espacios ni guiones.'
  }

  const password = data.password ?? ''
  if (requirePassword && !password) {
    errors.password = 'La contraseña es obligatoria.'
  } else if (password && password.trim().length < TUTOR_PASSWORD_MIN_LENGTH) {
    errors.password = `La contraseña debe tener al menos ${TUTOR_PASSWORD_MIN_LENGTH} caracteres.`
  }

  if (!data.dir_street.trim()) {
    errors.dir_street = 'La calle es obligatoria.'
  }
  if (!data.dir_col.trim()) {
    errors.dir_col = 'La colonia es obligatoria.'
  }
  if (!data.dir_num.trim()) {
    errors.dir_num = 'El número es obligatorio.'
  }

  return errors
}
