import { forwardRef } from 'react'
import Webcam from 'react-webcam'
import { Camera, CameraOff, RotateCcw } from 'lucide-react'
import Button from '../ui/Button.jsx'

const VIDEO_CONSTRAINTS = {
  width: 1280,
  height: 720,
  facingMode: 'user',
}

/**
 * Panel de captura de cámara para el enrolamiento biométrico (RF-02).
 * Tiene 3 estados: cámara apagada, feed en vivo (con guía ovalada) y foto
 * ya capturada. `ref` se reenvía al componente `Webcam` para poder tomar el
 * screenshot desde el componente padre.
 */
const WebcamCapture = forwardRef(function WebcamCapture(
  { cameraOn, onEnableCamera, capturedImage, onRetake, allChecksPassed },
  webcamRef,
) {
  return (
    <div className="relative flex aspect-video w-full items-center justify-center overflow-hidden rounded-xl border border-gray-200 bg-moss shadow-sm">
      {!cameraOn && !capturedImage && (
        <div className="flex flex-col items-center gap-4 px-6 text-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-white/10">
            <CameraOff className="h-8 w-8 text-gray-300" aria-hidden="true" />
          </div>
          <div>
            <p className="font-roboto text-sm font-medium text-gray-100">Cámara apagada</p>
            <p className="mt-1 max-w-xs font-lato text-xs text-gray-400">
              Enciende la cámara para iniciar la captura biométrica del alumno.
            </p>
          </div>
          <Button variant="primary" icon={Camera} onClick={onEnableCamera}>
            Encender Cámara
          </Button>
        </div>
      )}

      {cameraOn && !capturedImage && (
        <>
          <Webcam
            ref={webcamRef}
            audio={false}
            mirrored
            screenshotFormat="image/jpeg"
            videoConstraints={VIDEO_CONSTRAINTS}
            className="h-full w-full object-cover"
          />

          {/* Guía de silueta para encuadrar el rostro y los hombros */}
          <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
            <img
              src="/face.png"
              alt=""
              aria-hidden="true"
              className={`h-[88%] w-auto object-contain transition-[filter,opacity] duration-500
                ${allChecksPassed ? 'opacity-100' : 'opacity-70'}`}
              style={{
                filter: allChecksPassed
                  ? 'drop-shadow(0 0 10px rgba(155, 179, 154, 0.9))'
                  : 'drop-shadow(0 0 6px rgba(255, 255, 255, 0.35))',
              }}
            />
          </div>

          <span className="absolute left-4 top-4 inline-flex items-center gap-1.5 rounded-full bg-black/40 px-3 py-1 font-roboto text-xs text-white backdrop-blur-sm">
            <span className="h-1.5 w-1.5 rounded-full bg-red-500" aria-hidden="true" />
            En vivo
          </span>
        </>
      )}

      {capturedImage && (
        <>
          <img src={capturedImage} alt="Captura del rostro del alumno" className="h-full w-full object-cover" />
          <div className="absolute bottom-4 right-4">
            <Button variant="secondary" icon={RotateCcw} onClick={onRetake}>
              Retomar foto
            </Button>
          </div>
        </>
      )}
    </div>
  )
})

export default WebcamCapture
