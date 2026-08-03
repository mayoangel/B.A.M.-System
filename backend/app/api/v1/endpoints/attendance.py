from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from app.services.attendance_service import AttendanceServices
from app.schemas.attendance import AttendanceSchema

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')
attendance_schema = AttendanceSchema()

@attendance_bp.route('/', methods=['POST'])
def record_attendance():
    data = request.get_json() or {}
    try:
        attendance_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Datos de asistencia inválidos.", "details": err.messages}), 400
    try:
        service = AttendanceServices(g.db)
        result = service.registerAttendances(data)
        return jsonify({"message": "Asistencia registrada con éxito.", "id": result.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@attendance_bp.route('/student/<int:student_id>', methods=['GET'])
def get_student_attendance(student_id):
    try:
        service = AttendanceServices(g.db)
        records = service.getAttendanceByStudent(student_id)
        return jsonify([{"id": r.id, "date": str(r.date), "status": r.status} for r in records]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@attendance_bp.route('/student/<int:student_id>/date/<string:attendance_date>', methods=['GET'])
def get_student_attendance_by_date(student_id, attendance_date):
    try:
        service = AttendanceServices(g.db)
        records = service.getAttendanceByStudentAndDate(student_id, attendance_date)
        return jsonify([{"id": r.id, "date": str(r.date), "status": r.status, "course_id": r.course_id} for r in records]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@attendance_bp.route('/course/<int:course_id>', methods=['GET'])
def get_course_attendance(course_id):
    try:
        service = AttendanceServices(g.db)

        attendance_date = request.args.get("date")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if attendance_date:
            records = service.getAttendanceByCourseAndDate(course_id, attendance_date)
        elif start_date and end_date:
            records = service.getAttendanceByCourseAndDateRange(course_id, start_date, end_date)
        else:
            return jsonify({"error": "Proporciona 'date' o 'start_date' y 'end_date'"}), 400

        return jsonify([{"id": r.id, "date": str(r.date), "status": r.status, "student_id": r.student_id} for r in records]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@attendance_bp.route('/alerts/critical', methods=['GET'])
def get_critical_alerts():
    try:
        service = AttendanceServices(g.db)
        alerts = service.get_critical_absence_alerts()
        return jsonify(alerts), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400