import { useEffect, useRef } from 'react'
import Webcam from 'react-webcam'
import { Camera, CameraOff, Loader2 } from 'lucide-react'
import Button from '../ui/Button.jsx'

const VIDEO_CONSTRAINTS = {
  width: 1280,
  height: 720,
  facingMode: 'user',
}

// Cada cuánto se captura un cuadro para identificar un rostro. Deja margen
// de sobra frente al objetivo de rendimiento de `identify_user` (RF-03:
// idealmente 0.5-1.5s, tope 3s).
const SCAN_INTERVAL_MS = 2500

const STATUS_STYLES = {
  scanning: 'bg-black/50 text-gray-100',
  idle: 'bg-black/50 text-gray-100',
  success: 'bg-primary/90 text-white',
  info: 'bg-moss/90 text-white',
  warning: 'bg-amber-500/90 text-white',
  error: 'bg-red-500/90 text-white',
}

/**
 * Panel de cámara para el pase de lista (RF-03). A diferencia de
 * `WebcamCapture` (captura única para enrolamiento), este componente escanea
 * continuamente mientras la cámara esté encendida: cada `SCAN_INTERVAL_MS`
 * toma un cuadro y lo entrega a `onFrame`, que el componente padre usa para
 * identificar al alumno y registrar su asistencia.
 */
export default function AttendanceCamera({ cameraOn, onEnableCamera, onFrame, status }) {
  const webcamRef = useRef(null)
  const isBusyRef = useRef(false)

  useEffect(() => {
    if (!cameraOn) {
      return undefined
    }

    const interval = setInterval(() => {
      if (isBusyRef.current) {
        return
      }
      const frame = webcamRef.current?.getScreenshot()
      if (!frame) {
        return
      }

      isBusyRef.current = true
      Promise.resolve(onFrame(frame)).finally(() => {
        isBusyRef.current = false
      })
    }, SCAN_INTERVAL_MS)

    return () => clearInterval(interval)
  }, [cameraOn, onFrame])

  return (
    <div className="relative flex aspect-video w-full items-center justify-center overflow-hidden rounded-xl border border-gray-200 bg-moss shadow-sm">
      {!cameraOn && (
        <div className="flex flex-col items-center gap-4 px-6 text-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-white/10">
            <CameraOff className="h-8 w-8 text-gray-300" aria-hidden="true" />
          </div>
          <div>
            <p className="font-roboto text-sm font-medium text-gray-100">Cámara apagada</p>
            <p className="mt-1 max-w-xs font-lato text-xs text-gray-400">
              Enciende la cámara para reconocer automáticamente a los alumnos frente a ella.
            </p>
          </div>
          <Button variant="primary" icon={Camera} onClick={onEnableCamera}>
            Encender Cámara
          </Button>
        </div>
      )}

      {cameraOn && (
        <>
          <Webcam
            ref={webcamRef}
            audio={false}
            mirrored
            screenshotFormat="image/jpeg"
            videoConstraints={VIDEO_CONSTRAINTS}
            className="h-full w-full object-cover"
          />

          <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
            <img
              src="/face.png"
              alt=""
              aria-hidden="true"
              className="h-[88%] w-auto object-contain opacity-40"
            />
          </div>

          <span className="absolute left-4 top-4 inline-flex items-center gap-1.5 rounded-full bg-black/40 px-3 py-1 font-roboto text-xs text-white backdrop-blur-sm">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-red-500" aria-hidden="true" />
            Escaneando
          </span>

          {status && (
            <div
              className={`absolute inset-x-4 bottom-4 flex items-center gap-2 rounded-lg px-4 py-2.5 font-roboto
                text-sm backdrop-blur-sm transition-colors duration-300 ${STATUS_STYLES[status.type] ?? STATUS_STYLES.idle}`}
            >
              {status.type === 'scanning' && (
                <Loader2 className="h-4 w-4 shrink-0 animate-spin" aria-hidden="true" />
              )}
              <span>{status.text}</span>
            </div>
          )}
        </>
      )}
    </div>
  )
}
