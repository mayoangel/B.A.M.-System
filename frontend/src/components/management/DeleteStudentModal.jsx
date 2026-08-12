import { AlertTriangle, Fingerprint, Trash2 } from 'lucide-react'
import Modal from '../ui/Modal.jsx'
import Alert from '../ui/Alert.jsx'
import Button from '../ui/Button.jsx'

/**
 * Confirmación de baja de un alumno. Advierte explícitamente que su
 * información biométrica se eliminará de forma permanente (LFPDPPP): el
 * backend (`StudentService.delete_student_by_id`) limpia tanto la fila en
 * base de datos como la caché en memoria del motor de reconocimiento.
 */
export default function DeleteStudentModal({ student, onClose, onConfirm, isDeleting, error }) {
  return (
    <Modal title="Dar de baja al alumno" onClose={onClose} maxWidthClassName="max-w-md">
      <div className="flex flex-col gap-4">
        <div className="flex items-start gap-3">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-red-50 text-red-500">
            <AlertTriangle className="h-5 w-5" aria-hidden="true" />
          </span>
          <div>
            <p className="font-roboto text-sm font-semibold text-moss">
              {student.name} {student.lastname} ({student.id_student})
            </p>
            <p className="mt-1 font-lato text-sm text-gray-500">
              Esta acción elimina permanentemente el expediente del alumno, su inscripción a
              cursos y su historial de asistencia. No se puede deshacer.
            </p>
          </div>
        </div>

        <Alert variant="warning" title="Se eliminará también su información biométrica">
          <div className="flex items-start gap-2">
            <Fingerprint className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
            <span>
              El vector facial enrolado de este alumno se borrará de forma permanente, tanto de la
              base de datos como de la memoria del sistema de reconocimiento, conforme a la
              LFPDPPP.
            </span>
          </div>
        </Alert>

        {error && (
          <Alert variant="error" title="No se pudo completar la baja">
            {error}
          </Alert>
        )}

        <div className="flex justify-end gap-3 border-t border-gray-100 pt-4">
          <Button variant="ghost" onClick={onClose} disabled={isDeleting}>
            Cancelar
          </Button>
          <Button
            variant="primary"
            icon={Trash2}
            loading={isDeleting}
            onClick={onConfirm}
            className="!bg-red-500 hover:!bg-red-600 focus-visible:!ring-red-300"
          >
            Dar de baja
          </Button>
        </div>
      </div>
    </Modal>
  )
}
