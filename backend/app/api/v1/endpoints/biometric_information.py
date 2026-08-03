from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from app.services.biometric_service import BiometricService
from app.services.biometric_exceptions import BiometricError
from app.schemas.biometric_information import BiometricInformationSchema

biometric_bp = Blueprint('biometric', __name__)
biometric_schema = BiometricInformationSchema()

# Mapeo de excepciones de dominio -> código HTTP. Todo lo que no esté aquí
# cae en 422 (imagen/rostro inválidos) por defecto.
_ERROR_STATUS_MAP = {
    "AlreadyEnrolledError": 409,
    "DuplicateFaceError": 409,
    "NoEnrolledFacesError": 404,
    "FaceNotRecognizedError": 404,
}


def _status_for(error: BiometricError) -> int:
    return _ERROR_STATUS_MAP.get(type(error).__name__, 422)


@biometric_bp.route('/', methods=['POST'])
def register_biometric():
    """Alta manual de un vector ya calculado externamente (uso administrativo)."""
    data = request.get_json() or {}
    try:
        biometric_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos biométricos inválidos.", "details": err.messages}), 400
    try:
        service = BiometricService(g.db)
        result = service.register_biometric(data)
        return jsonify({"message": "Información biométrica asociada correctamente.", "id": result.id}), 201
    except BiometricError as e:
        return jsonify({"error": str(e)}), _status_for(e)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@biometric_bp.route('/enroll', methods=['POST'])
def enroll_user():
    """RF-02: enrola el rostro de un usuario a partir de una foto capturada por la cámara."""
    image_file = request.files.get('image')
    user_id = request.form.get('user_id', type=int)

    if image_file is None:
        return jsonify({"error": "Se requiere el archivo de imagen 'image' (multipart/form-data)."}), 400
    if not user_id:
        return jsonify({"error": "Se requiere el campo 'user_id'."}), 400

    try:
        service = BiometricService(g.db)
        result = service.enroll_user(image_file.read(), user_id)
        return jsonify({
            "message": "Enrolamiento biométrico completado correctamente.",
            "id": result.id,
            "student_id": result.student_id
        }), 201
    except BiometricError as e:
        return jsonify({"error": str(e)}), _status_for(e)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@biometric_bp.route('/identify', methods=['POST'])
def identify_user():
    """RF-03: identifica en tiempo real a la persona frente a la cámara para pasar asistencia."""
    image_file = request.files.get('image')

    if image_file is None:
        return jsonify({"error": "Se requiere el archivo de imagen 'image' (multipart/form-data)."}), 400

    try:
        service = BiometricService(g.db)
        result = service.identify_user(image_file.read())
        return jsonify(result), 200
    except BiometricError as e:
        return jsonify({"error": str(e)}), _status_for(e)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@biometric_bp.route('/student/<int:student_id>', methods=['GET'])
def get_biometric_by_student(student_id):
    try:
        service = BiometricService(g.db)
        biometric = service.get_biometric_by_student_id(student_id)
        return jsonify({"id": biometric.id, "biometric_type": "Facial", "status": "Registrado"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@biometric_bp.route('/student/<int:student_id>', methods=['DELETE'])
def delete_biometric(student_id):
    try:
        service = BiometricService(g.db)
        service.delete_biometric(student_id)
        return jsonify({"message": "Información biométrica eliminada correctamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
