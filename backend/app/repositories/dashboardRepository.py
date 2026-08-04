from datetime import date
from sqlalchemy import func

from app.models.students import Students
from app.models.attendance import Attendance
from app.models.courses import Courses
from app.models.student_courses import StudentCourses
from datetime import timedelta


##### AGREGADO PARA EL DASBOARD ######  


class DashboardRepository:

    ## OBTIENE EL RESUMEN PARA EL DASBOARD ###
    ### Total de estudiantes
    ### Asistencias de hoy
    ### Grupos activos
    ### Alertas pendientes
    def get_summary(self, db):

        today = date.today()

        total_students = db.query(Students).count()

        present_today = (
            db.query(Attendance)
            .filter(
                Attendance.date == today,
                ##Attendance.status == "Presente"
                Attendance.status.in_(
                    ["Asistencia", "Retardo"]
                )
            )
            .count()
        )

        total_today = (
            db.query(Attendance)
            .filter(
                Attendance.date == today
            )
            .count()
        )

        attendance_percentage = (
            round((present_today / total_today) * 100, 2)
            if total_today > 0 else 0
        )

        active_groups = db.query(Courses).count()

        return {
            "total_students": total_students,
            "attendance_today": attendance_percentage,
            "active_groups": active_groups,
            "pending_alerts": 0
        }


    ###  OBTIENE ESTUDIANTES POR CURSOS ##

    def get_courses_distribution(self, db):



        #### StudentCourses
        
        result = (
            db.query(
                Courses.id,
                Courses.name,
                func.count(
                    StudentCourses.student_id
                ).label("students")
            )
            .join(
                StudentCourses,
                Courses.id == StudentCourses.course_id
            )
            .group_by(
                Courses.id,
                Courses.name
            )
            .all()
        )

        return [
            {
                "course_id": row.id,
                "course": row.name,
                "students": row.students
            }
            for row in result
        ]
    
    ### KPI GENERAL ###

    def get_kpis(self, db):

        total = db.query(Attendance).count()

        attendance = (
            db.query(Attendance)
            .filter(
                Attendance.status.in_(
                    ["Asistencia", "Retardo"]
                )
            )
            .count()
        )

        absent = (
            db.query(Attendance)
            .filter(
                Attendance.status == "Falta"
            )
            .count()
        )

        percentage = (
            round(
                (attendance / total) * 100,
                2
            )
            if total > 0 else 0
        )

        return {
            "general_attendance": percentage,
            "attendance": attendance,
            "absent": absent
        }
    


    ####
    ####
    def get_history(
        self,
        db,
        student_id=None,
        course_id=None,
        start_date=None,
        end_date=None
    ):

        query = (
            db.query(Attendance)
            .join(Students)
        )

        if student_id:

            query = query.filter(
                Attendance.student_id == student_id
            )

        if course_id:

            query = (
                query
                .join(
                    StudentCourses,
                    Attendance.student_id ==
                    StudentCourses.student_id
                )
                .filter(
                    StudentCourses.course_id == course_id
                )
            )

        if start_date:

            query = query.filter(
                Attendance.date >= start_date
            )

        if end_date:

            query = query.filter(
                Attendance.date <= end_date
            )

        records = query.all()

        return [
            {
                "student_id": record.student_id,
                "student": record.students.name,
                "lastname": record.students.lastname,
                "date": str(record.date),
                "time": str(record.time),
                "status": record.status,
                "method": record.method
            }
            for record in records
        ]
    

    def get_weekly_attendance(self, db):

        last_records = (
            db.query(Attendance)
            .order_by(
                Attendance.date.desc()
            )
            .all()
        )

        grouped = {}

        for record in last_records:

            day = str(record.date)

            if day not in grouped:

                grouped[day] = {
                    "total": 0,
                    "present": 0
                }

            grouped[day]["total"] += 1

            if record.status in [
                "Asistencia",
                "Retardo"
                ]:
                grouped[day]["present"] += 1

        result = []

        for day, values in grouped.items():

            percentage = (
                round(
                    (
                        values["present"]
                        /
                        values["total"]
                    ) * 100,
                    2
                )
                if values["total"] > 0
                else 0
            )

            result.append({
                "date": day,
                "attendance": percentage
            })

        return result[:7]

            


            
            