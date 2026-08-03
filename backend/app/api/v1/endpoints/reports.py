from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.core.database import get_db
from app.services.report_service import ReportService
from app.schemas.reports import ReportSchema

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
report_schema = ReportSchema()

@reports_bp.route('/', methods=['POST'])
def create_report():
    db = get_db()
    report_data = request.get_json() or {}
    try:
        report_schema.load(report_data)
    except ValidationError as err:
        return jsonify({"error": "Datos de reporte inválidos.", "details": err.messages}), 400
    try:
        service = ReportService(db)
        result = service.register_report(report_data)
        return jsonify({"message": f"Reporte '{result.name}' guardado.", "id": result.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@reports_bp.route('/', methods=['GET'])
def get_all_reports():
    db = get_db()
    try:
        service = ReportService(db)
        reports = service.list_all_reports()
        return jsonify([{
            "id": r.id,
            "name": r.name,
            "generation_date": r.generation_date.strftime("%Y-%m-%d %H:%M:%S"),
            "employee_id": r.employee_id
        } for r in reports]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reports_bp.route('/filter', methods=['GET'])
def get_reports_by_date():
    db = get_db()
    date_str = request.args.get('date', '')
    try:
        service = ReportService(db)
        reports = service.get_reports_by_date(date_str)
        return jsonify([{
            "id": r.id,
            "name": r.name,
            "generation_date": r.generation_date.strftime("%Y-%m-%d %H:%M:%S"),
            "employee_id": r.employee_id
        } for r in reports]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@reports_bp.route('/<string:name>', methods=['GET'])
def get_report(name):
    db = get_db()
    try:
        service = ReportService(db)
        report = service.get_report_by_name(name)
        return jsonify({"id": report.id, "name": report.name}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@reports_bp.route('/<string:name>', methods=['PUT'])
def update_report(name):
    db = get_db()
    new_data = request.get_json() or {}
    try:
        report_schema.load(new_data, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos de reporte inválidos.", "details": err.messages}), 400
    try:
        service = ReportService(db)
        service.update_report(name, new_data)
        return jsonify({"message": f"Reporte '{name}' actualizado correctamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@reports_bp.route('/<string:name>', methods=['DELETE'])
def delete_report(name):
    db = get_db()
    try:
        service = ReportService(db)
        service.delete_report(name)
        return jsonify({"message": f"Reporte '{name}' eliminado correctamente."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400