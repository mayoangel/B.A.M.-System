from flask import Blueprint, jsonify, request
from app.core.database import get_db
from app.services.non_working_days_services import NonWorkingDaysService

non_working_days_bp = Blueprint('non_working_days', __name__, url_prefix='/api/v1/calendar')

@non_working_days_bp.route('', methods=['GET'])
def get_all_days():
    db = next(get_db())
    service = NonWorkingDaysService(db)
    days = service.list_all_days()
    
    return jsonify([{
        "id": d.id,
        "date": d.date.strftime("%Y-%m-%d"),
        "description": d.description
    } for d in days]), 200

@non_working_days_bp.route('', methods=['POST'])
def create_day():
    data = request.get_json() or {}
    date_str = data.get("date")
    description = data.get("description")

    if not date_str or not description:
        return jsonify({"error": "Los campos 'date' y 'description' son obligatorios."}), 400

    db = next(get_db())
    try:
        service = NonWorkingDaysService(db)
        new_day = service.add_non_working_day(date_str, description)
        return jsonify({
            "message": "Día inhábil registrado con éxito.",
            "day": {
                "id": new_day.id,
                "date": new_day.date.strftime("%Y-%m-%d"),
                "description": new_day.description
            }
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@non_working_days_bp.route('/<int:id>', methods=['DELETE'])
def delete_day(id):
    db = next(get_db())
    try:
        service = NonWorkingDaysService(db)
        result = service.delete_non_working_day(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404