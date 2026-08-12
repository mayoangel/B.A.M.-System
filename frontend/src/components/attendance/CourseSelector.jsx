import { BookOpen, Calendar, Loader2 } from 'lucide-react'
import Alert from '../ui/Alert.jsx'

/**
 * Selección de curso para iniciar una sesión de pase de lista. Muestra los
 * cursos activos como tarjetas; al elegir uno se dispara `onSelectCourse`.
 */
export default function CourseSelector({ courses, loading, error, onSelectCourse }) {
  return (
    <section className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm sm:p-8">
      <h2 className="font-roboto text-base font-semibold text-moss">Selecciona un curso</h2>
      <p className="mt-1 font-lato text-sm text-gray-500">
        Elige el curso para iniciar la sesión de pase de lista biométrico.
      </p>

      {error && (
        <Alert variant="error" title="No se pudieron cargar los cursos" className="mt-4">
          {error}
        </Alert>
      )}

      {loading ? (
        <div className="mt-8 flex items-center justify-center gap-2 py-12 text-gray-400">
          <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
          <span className="font-lato text-sm">Cargando cursos...</span>
        </div>
      ) : (
        <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {courses.map((course) => (
            <button
              key={course.id}
              type="button"
              onClick={() => onSelectCourse(course)}
              className="flex flex-col items-start gap-3 rounded-xl border border-gray-100 bg-white p-5 text-left shadow-sm
                transition-colors hover:border-primary hover:bg-mint/40 focus:outline-none
                focus-visible:ring-2 focus-visible:ring-primary/40"
            >
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-mint text-primary">
                <BookOpen className="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <p className="font-roboto text-sm font-semibold text-moss">{course.name}</p>
                <p className="mt-1 font-lato text-xs text-gray-500">{course.category}</p>
              </div>
              <span className="mt-auto inline-flex items-center gap-1.5 font-lato text-xs text-gray-400">
                <Calendar className="h-3.5 w-3.5" aria-hidden="true" />
                {course.days_of_week || 'Horario sin definir'}
              </span>
            </button>
          ))}
          {courses.length === 0 && (
            <p className="col-span-full py-8 text-center font-lato text-sm text-gray-400">
              No hay cursos activos disponibles.
            </p>
          )}
        </div>
      )}
    </section>
  )
}
