import { useMemo, useState } from 'react'
import { BookOpen, CalendarDays, Clock, Layers, Save, Tag } from 'lucide-react'
import Modal from '../ui/Modal.jsx'
import TextInput from '../ui/TextInput.jsx'
import SelectInput from '../ui/SelectInput.jsx'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'
import { createCourse } from '../../api/courses.js'
import { ApiError } from '../../api/client.js'

const STATUS_OPTIONS = [
  { value: 'Activo', label: 'Activo' },
  { value: 'Inactivo', label: 'Inactivo' },
]

const INITIAL_FORM = {
  name: '',
  description: '',
  category: '',
  start_date: '',
  end_date: '',
  time_duration: '',
  days_of_week: '',
  status: 'Activo',
}

function validateCourseForm(data) {
  const errors = {}
  if (!data.name.trim() || data.name.trim().length < 2) {
    errors.name = 'El nombre debe tener al menos 2 caracteres.'
  }
  if (!data.description.trim()) {
    errors.description = 'La descripción es obligatoria.'
  }
  if (!data.category.trim()) {
    errors.category = 'La categoría es obligatoria.'
  }
  if (!data.start_date) {
    errors.start_date = 'La fecha de inicio es obligatoria.'
  }
  if (!data.end_date) {
    errors.end_date = 'La fecha de fin es obligatoria.'
  } else if (data.start_date && data.end_date <= data.start_date) {
    errors.end_date = 'La fecha de fin debe ser posterior a la de inicio.'
  }
  if (!data.time_duration.trim()) {
    errors.time_duration = 'La duración es obligatoria.'
  }
  if (!data.days_of_week.trim()) {
    errors.days_of_week = 'Indica los días de la semana (ej. Lun, Mie, Vie).'
  }
  return errors
}

/**
 * Modal para dar de alta un curso nuevo. Los campos coinciden con
 * `CourseSchema` del backend.
 */
export default function CreateCourseModal({ onClose, onCreated }) {
  const [form, setForm] = useState(INITIAL_FORM)
  const [attempted, setAttempted] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  const errors = useMemo(() => validateCourseForm(form), [form])
  const isValid = Object.keys(errors).length === 0

  function handleChange(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  async function handleSubmit() {
    setAttempted(true)
    setError(null)
    if (!isValid) return

    setSaving(true)
    try {
      const result = await createCourse({
        name: form.name.trim(),
        description: form.description.trim(),
        category: form.category.trim(),
        start_date: form.start_date,
        end_date: form.end_date,
        time_duration: form.time_duration.trim(),
        days_of_week: form.days_of_week.trim(),
        status: form.status,
      })
      onCreated(result)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'No se pudo crear el curso.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Modal title="Nuevo curso" onClose={onClose} maxWidthClassName="max-w-2xl">
      <div className="flex flex-col gap-5">
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
          <TextInput
            label="Nombre del curso"
            icon={BookOpen}
            value={form.name}
            onChange={(e) => handleChange('name', e.target.value)}
            error={attempted ? errors.name : undefined}
            required
            containerClassName="sm:col-span-2"
          />
          <TextInput
            label="Descripción"
            icon={Layers}
            value={form.description}
            onChange={(e) => handleChange('description', e.target.value)}
            error={attempted ? errors.description : undefined}
            required
            containerClassName="sm:col-span-2"
          />
          <TextInput
            label="Categoría"
            icon={Tag}
            placeholder="Tecnología, Diseño..."
            value={form.category}
            onChange={(e) => handleChange('category', e.target.value)}
            error={attempted ? errors.category : undefined}
            required
          />
          <SelectInput
            label="Estatus"
            value={form.status}
            onChange={(e) => handleChange('status', e.target.value)}
            options={STATUS_OPTIONS}
          />
          <TextInput
            label="Fecha de inicio"
            icon={CalendarDays}
            type="date"
            value={form.start_date}
            onChange={(e) => handleChange('start_date', e.target.value)}
            error={attempted ? errors.start_date : undefined}
            required
          />
          <TextInput
            label="Fecha de fin"
            icon={CalendarDays}
            type="date"
            value={form.end_date}
            onChange={(e) => handleChange('end_date', e.target.value)}
            error={attempted ? errors.end_date : undefined}
            required
          />
          <TextInput
            label="Duración"
            icon={Clock}
            placeholder="80 horas"
            value={form.time_duration}
            onChange={(e) => handleChange('time_duration', e.target.value)}
            error={attempted ? errors.time_duration : undefined}
            required
          />
          <TextInput
            label="Días de la semana"
            icon={CalendarDays}
            placeholder="Lun, Mie, Vie"
            value={form.days_of_week}
            onChange={(e) => handleChange('days_of_week', e.target.value)}
            error={attempted ? errors.days_of_week : undefined}
            required
          />
        </div>

        {attempted && !isValid && (
          <Alert variant="error" title="Revisa los campos marcados en rojo">
            Completa los datos obligatorios del curso antes de guardar.
          </Alert>
        )}
        {error && (
          <Alert variant="error" title="No se pudo crear el curso">
            {error}
          </Alert>
        )}

        <div className="flex justify-end gap-3 border-t border-gray-100 pt-5">
          <Button variant="ghost" onClick={onClose} disabled={saving}>
            Cancelar
          </Button>
          <Button variant="primary" icon={Save} loading={saving} onClick={handleSubmit}>
            Crear curso
          </Button>
        </div>
      </div>
    </Modal>
  )
}
