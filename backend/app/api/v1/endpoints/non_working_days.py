from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.core.database import get_db
from app.services.non_working_days_service import NonWorkingDaysService
from app.schemas.non_working_days import NonWorkingDaySchema

non_working_days_bp = Blueprint('non_working_days', __name__, url_prefix='/api/v1/calendar')
non_working_day_schema = NonWorkingDaySchema()

@non_working_days_bp.route('/', methods=['GET'])
def get_all_days():
    db = get_db()
    service = NonWorkingDaysService(db)
    days = service.list_all_days()
    
    return jsonify([{
        "id": d.id,
        "date": d.date.strftime("%Y-%m-%d"),
        "description": d.description
    } for d in days]), 200

@non_working_days_bp.route('/', methods=['POST'])
def create_day():
    data = request.get_json() or {}
    try:
        # Se valida el formato (fecha ISO, descripción no vacía), pero se conserva
        # `date_str` como texto porque `NonWorkingDaysService` lo parsea internamente.
        non_working_day_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos.", "details": err.messages}), 400

    date_str = data.get("date")
    description = data.get("description")

    db = get_db()
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
    db = get_db()
    try:
        service = NonWorkingDaysService(db)
        result = service.delete_non_working_day(id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404