import { useEffect } from 'react'
import { X } from 'lucide-react'

/**
 * Modal genérico y minimalista: fondo semitransparente, cierre con Escape o
 * clic fuera del panel, y encabezado con título + botón de cerrar. Usado por
 * las pantallas de administración (edición y confirmaciones destructivas).
 */
export default function Modal({ title, children, onClose, maxWidthClassName = 'max-w-2xl' }) {
  useEffect(() => {
    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        onClose()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4 py-8"
      onClick={onClose}
    >
      <div
        className={`flex max-h-full w-full ${maxWidthClassName} flex-col overflow-hidden rounded-xl bg-white shadow-xl`}
        onClick={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="flex items-center justify-between border-b border-gray-100 px-6 py-4">
          <h2 className="font-roboto text-base font-semibold text-moss">{title}</h2>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-gray-400 transition-colors hover:bg-gray-100 hover:text-moss
              focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/30"
            aria-label="Cerrar"
          >
            <X className="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto px-6 py-6">{children}</div>
      </div>
    </div>
  )
}
