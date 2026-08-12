import { BookOpen, Building2, Home, Lock, Mail, MapPin, Phone, User } from 'lucide-react'
import TextInput from '../ui/TextInput.jsx'
import SelectInput from '../ui/SelectInput.jsx'
import Alert from '../ui/Alert.jsx'

/**
 * Paso 3: Tutor y Curso.
 *
 * El alumno es menor de edad y no tiene un tutor pre-registrado: aquí se
 * capturan los datos completos del tutor (que se envían a `POST /parents/`
 * antes de crear al alumno). El curso es opcional: si se deja sin
 * seleccionar, el alumno se registra sin inscripción inicial.
 */
export default function TutorCourseForm({
  data,
  onChange,
  errors = {},
  courses,
  coursesLoading,
  coursesError,
}) {
  const handleChange = (field) => (event) => onChange(field, event.target.value)

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="mb-4 font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
          Datos del tutor
        </h3>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
          <TextInput
            label="Nombre(s)"
            icon={User}
            placeholder="Ej. Carlos"
            value={data.name}
            onChange={handleChange('name')}
            error={errors.name}
            required
          />
          <TextInput
            label="Apellidos"
            icon={User}
            placeholder="Ej. Mendoza Ruiz"
            value={data.lastname}
            onChange={handleChange('lastname')}
            error={errors.lastname}
            required
          />
          <TextInput
            label="Correo electrónico"
            icon={Mail}
            type="email"
            placeholder="tutor@correo.com"
            value={data.email}
            onChange={handleChange('email')}
            error={errors.email}
            required
          />
          <TextInput
            label="Teléfono"
            icon={Phone}
            type="tel"
            placeholder="10 dígitos"
            value={data.phone}
            onChange={handleChange('phone')}
            error={errors.phone}
            required
          />
          <TextInput
            label="Contraseña"
            icon={Lock}
            type="password"
            placeholder="Mínimo 8 caracteres"
            hint="Se usará para el acceso del tutor al portal."
            value={data.password}
            onChange={handleChange('password')}
            error={errors.password}
            required
          />
          <TextInput
            label="Calle"
            icon={MapPin}
            value={data.dir_street}
            onChange={handleChange('dir_street')}
            error={errors.dir_street}
            required
          />
          <TextInput
            label="Colonia"
            icon={Building2}
            value={data.dir_col}
            onChange={handleChange('dir_col')}
            error={errors.dir_col}
            required
          />
          <TextInput
            label="Número"
            icon={Home}
            value={data.dir_num}
            onChange={handleChange('dir_num')}
            error={errors.dir_num}
            required
          />
        </div>
      </div>

      <div>
        <h3 className="mb-4 font-roboto text-sm font-semibold uppercase tracking-wide text-primary">
          Curso
        </h3>

        {coursesError && (
          <Alert variant="warning" title="No se pudieron cargar los cursos activos">
            {coursesError}
          </Alert>
        )}

        <SelectInput
          label="Curso"
          icon={BookOpen}
          placeholder={coursesLoading ? 'Cargando cursos…' : 'Sin asignar por ahora'}
          value={data.course_id}
          onChange={handleChange('course_id')}
          error={errors.course_id}
          disabled={coursesLoading}
          options={courses.map((course) => ({ value: String(course.id), label: course.name }))}
          hint="Opcional: puedes asignar el curso más adelante."
        />
      </div>
    </div>
  )
}
