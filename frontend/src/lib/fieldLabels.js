/** Traducciones legibles para los nombres de campo que devuelve Marshmallow en `details`. */
export const FIELD_LABELS = {
  id_student: 'Matrícula',
  name: 'Nombre(s)',
  lastname: 'Apellido(s)',
  surename: 'Apellido materno',
  date_of_birth: 'Fecha de nacimiento',
  email: 'Correo electrónico',
  password: 'Contraseña',
  phone: 'Teléfono',
  dir_street: 'Calle',
  dir_col: 'Colonia',
  dir_num: 'Número',
  id_parent: 'Tutor',
  course_id: 'Curso',
  status: 'Estatus',
  student_id: 'Alumno',
  user_id: 'Alumno',
  image: 'Fotografía',
}

export function labelForField(field) {
  return FIELD_LABELS[field] ?? field.replaceAll('_', ' ')
}
