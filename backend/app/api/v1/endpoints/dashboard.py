from flask import Blueprint
from flask import jsonify
from flask import g

from flask_jwt_extended import jwt_required

from app.services.dashboard_service import DashboardService
from app.core.permissions import admin_required, staff_required, authenticated_required
from flask_jwt_extended import jwt_required
from flask import request

##### AGREGADO PARA EL DASBOARD ###### 


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

service = DashboardService()


@dashboard_bp.route(
    "/summary",
    methods=["GET"]
)
@jwt_required()
@admin_required
def get_summary():

    result = service.get_summary(g.db)

    return jsonify(result), 200


@dashboard_bp.route(
    "/courses",
    methods=["GET"]
)
@jwt_required()
@admin_required
def get_courses_distribution():

    result = service.get_courses_distribution(g.db)

    return jsonify(result), 200


@dashboard_bp.route(
    "/kpis",
    methods=["GET"]
)
@jwt_required()
@admin_required
def get_kpis():

    result = service.get_kpis(g.db)

    return jsonify(result), 200


####
###
@dashboard_bp.route(
    "/history",
    methods=["GET"]
)
@jwt_required()
@admin_required
def get_history():

    student_id = request.args.get(
        "student_id"
    )

    course_id = request.args.get(
        "course_id"
    )

    start_date = request.args.get(
        "start_date"
    )

    end_date = request.args.get(
        "end_date"
    )

    result = service.get_history(
        g.db,
        student_id,
        course_id,
        start_date,
        end_date
    )

    return jsonify(result), 200


@dashboard_bp.route(
    "/weekly-attendance",
    methods=["GET"]
)
@jwt_required()
@admin_required
def get_weekly_attendance():

    result = service.get_weekly_attendance(
        g.db
    )

    return jsonify(result), 200