import { Cake, User } from 'lucide-react'
import TextInput from '../ui/TextInput.jsx'

/**
 * Paso 2: Datos del Alumno.
 *
 * El alumno es menor de edad: no tiene credenciales, correo, teléfono ni
 * dirección propios (esos datos se recolectan del tutor en el Paso 3). La
 * matrícula (`id_student`) la genera automáticamente el backend, por lo que
 * aquí solo se capturan los datos mínimos de identidad, alineados con
 * `StudentSchema` (backend/app/schemas/students.py).
 */
export default function StudentDataForm({ data, onChange, errors = {} }) {
  const handleChange = (field) => (event) => onChange(field, event.target.value)

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
      <TextInput
        label="Nombre(s)"
        icon={User}
        placeholder="Ej. María José"
        value={data.name}
        onChange={handleChange('name')}
        error={errors.name}
        required
      />
      <TextInput
        label="Apellido paterno"
        icon={User}
        value={data.lastname}
        onChange={handleChange('lastname')}
        error={errors.lastname}
        required
      />
      <TextInput
        label="Apellido materno"
        icon={User}
        hint="Opcional"
        value={data.surename}
        onChange={handleChange('surename')}
        error={errors.surename}
      />
      <TextInput
        label="Fecha de nacimiento"
        icon={Cake}
        type="date"
        value={data.date_of_birth}
        onChange={handleChange('date_of_birth')}
        error={errors.date_of_birth}
        required
      />
    </div>
  )
}
