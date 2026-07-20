from flask import Blueprint, request, jsonify, g
from app.services.biometric_services import BiometricService 

biometric_bp = Blueprint('biometric', __name__)

@biometric_bp.route('/', methods=['POST'])
def register_biometric():
    data = request.get_json() or {}
    try:
        service = BiometricService(g.db)
        result = service.register_biometric(data)
        return jsonify({"message": "Información biométrica asociada correctamente.", "id": result.id}), 201
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