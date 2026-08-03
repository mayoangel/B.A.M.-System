import { apiDelete, apiPostFormData } from './client.js'

/**
 * Convierte un data URL en base64 (el que produce `webcam.getScreenshot()`)
 * en un `Blob` binario, listo para adjuntarse a un `FormData`.
 */
export function dataUrlToBlob(dataUrl) {
  const [header, base64Data] = dataUrl.split(',')
  const mimeMatch = header.match(/data:(.*?);base64/)
  const mimeType = mimeMatch ? mimeMatch[1] : 'image/jpeg'

  const binaryString = atob(base64Data)
  const bytes = new Uint8Array(binaryString.length)
  for (let i = 0; i < binaryString.length; i += 1) {
    bytes[i] = binaryString.charCodeAt(i)
  }

  return new Blob([bytes], { type: mimeType })
}

/**
 * RF-02: enrola el rostro de un alumno ya registrado.
 * Envía la imagen como multipart/form-data al endpoint `/biometrics/enroll`.
 */
export function enrollBiometrics(studentId, imageDataUrl) {
  const imageBlob = dataUrlToBlob(imageDataUrl)
  const formData = new FormData()
  formData.append('image', imageBlob, 'captura.jpg')
  formData.append('user_id', String(studentId))

  return apiPostFormData('/biometrics/enroll', formData)
}

/**
 * RF-03: identifica a la persona frente a la cámara comparando contra los
 * rostros enrolados. Usado en el pase de lista automatizado.
 * Devuelve `{ student_id, confidence, processing_time_seconds }` si hay
 * coincidencia; lanza `ApiError` si no se detecta/reconoce el rostro.
 */
export function identifyFace(imageDataUrl) {
  const imageBlob = dataUrlToBlob(imageDataUrl)
  const formData = new FormData()
  formData.append('image', imageBlob, 'captura.jpg')

  return apiPostFormData('/biometrics/identify', formData)
}

/**
 * Elimina de forma permanente la información biométrica de un alumno (fila
 * en base de datos y caché en memoria). Se usa antes de re-enrolar un nuevo
 * rostro (el backend rechaza `enroll` si ya existe uno) y al dar de baja al
 * alumno (LFPDPPP).
 */
export function deleteBiometrics(studentId) {
  return apiDelete(`/biometrics/student/${studentId}`)
}
