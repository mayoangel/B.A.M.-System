# Instrucciones para Claude - B.A.M. System

## Contexto General del Proyecto
*   **Nombre del Proyecto**: B.A.M. (Biometric Attendance & Management) System.
*   **Propósito**: Sistema web de gestión escolar con tecnología de reconocimiento facial para automatizar el registro de asistencia en organizaciones sin fines de lucro.
*   **Impacto**: Elimina el tiempo perdido en el pase de lista manual y provee métricas para prevenir la deserción escolar.

## Stack Tecnológico
*   **Frontend**: React y JavaScript.
*   **Backend (API)**: Python.
*   **Base de Datos**: Relacional (gestionada mediante scripts SQL puros en la carpeta `/database/`).
*   **Motor de Reconocimiento Facial**: Python (OpenCV, InsightFace, ONNX Runtime).

## Arquitectura de N-Capas (Clean Architecture)
El código dentro de `/backend/app/` DEBE estar estrictamente desacoplado aplicando los principios de Arquitectura Limpia. No debes mezclar lógica de negocio con definiciones de rutas HTTP o consultas SQL. Respeta esta estructura:
*   `api/` (o `routers/`): Capa de Presentación. Contiene los endpoints. Su única responsabilidad es recibir la petición HTTP, llamar al servicio correspondiente y devolver la respuesta.
*   `services/`: Capa de Dominio/Lógica de Negocio. Aquí viven las reglas de validación (ej. RF-01, RF-02) y la integración con el hardware o biometría. Nunca ejecutan SQL directamente.
*   `repositories/`: Capa de Datos/Infraestructura. Exclusivo para la comunicación con la base de datos.
*   `schemas/` (o `models/`): Definiciones de las estructuras de datos, validadores y DTOs (Data Transfer Objects).
*   `core/`: Configuraciones globales, inyección de dependencias, seguridad (JWT) y manejo de variables de entorno.

## Reglas Estrictas de Seguridad (Cumplimiento LFPDPPP)
*   **Contraseñas**: Obligatorio el uso de algoritmos hash seguros. Nunca guardar texto plano.
*   **Datos Biométricos**: El vector facial debe almacenarse estrictamente encriptado.
*   **Baja de Usuarios**: Al eliminar un usuario, su vector biométrico asociado debe ser eliminado permanentemente.
*   **Sesiones**: Implementar tokens firmados (JWT), expiración por inactividad y ruta segura de logout.

## Reglas de Rendimiento y Convenciones
*   **Biometría**: El procesamiento de captura y comparación de rostros debe tomar menos de 3 segundos (ideal: 0.5 a 1.5 segundos por rostro).
*   **Fallback**: Toda funcionalidad biométrica debe permitir el registro manual de asistencia (RF-08).