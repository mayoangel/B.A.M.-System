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
        yesterday = today - timedelta(days=1)
        first_day_current_month = date(today.year, today.month, 1)
        first_day_last_month = date(today.year, today.month - 1, 1) if today.month > 1 else date(today.year - 1, 12, 1)
        last_day_last_month = first_day_current_month - timedelta(days=1)

        # ===== TOTAL ESTUDIANTES =====
        total_students = db.query(Students).count()

        # Estudiantes del mes pasado (para calcular crecimiento)
        students_last_month = (
            db.query(Students)
            .filter(Students.created_at <= last_day_last_month)
            .count()
        )
        
        if students_last_month > 0:
            students_growth = round(((total_students - students_last_month) / students_last_month) * 100, 0)
        else:
            students_growth = 0

        # ===== ASISTENCIA HOY =====
        # Presentes hoy (Asistencia + Retardo)
        present_today = (
            db.query(Attendance)
            .filter(
                Attendance.date == today,
                Attendance.status.in_(["Asistencia", "Retardo"])
            )
            .count()
        )

        # Total de asistencias registradas hoy
        total_today = (
            db.query(Attendance)
            .filter(Attendance.date == today)
            .count()
        )

        # Porcentaje de asistencia hoy
        attendance_percentage = (
            round((present_today / total_today) * 100, 2)
            if total_today > 0 else 0
        )

        # ===== ASISTENCIA AYER (para comparación) =====
        present_yesterday = (
            db.query(Attendance)
            .filter(
                Attendance.date == yesterday,
                Attendance.status.in_(["Asistencia", "Retardo"])
            )
            .count()
        )

        total_yesterday = (
            db.query(Attendance)
            .filter(Attendance.date == yesterday)
            .count()
        )

        attendance_yesterday_percentage = (
            round((present_yesterday / total_yesterday) * 100, 2)
            if total_yesterday > 0 else 0
        )

        # Cambio porcentual vs ayer
        if attendance_yesterday_percentage > 0:
            attendance_change = round(
                ((attendance_percentage - attendance_yesterday_percentage) / attendance_yesterday_percentage) * 100, 
                1
            )
        else:
            attendance_change = 0

        # ===== GRUPOS ACTIVOS =====
        active_groups = db.query(Courses).filter(Courses.status == "Activo").count()
        
        # Total de cursos diferentes (todos, no solo activos)
        total_courses = db.query(Courses).count()

        # ===== ALERTAS PENDIENTES =====
        # Ejemplo: estudiantes con bajo rendimiento o inactivos
        # Puedes personalizar esta lógica según tus necesidades
        pending_alerts = 0
        
        # Ejemplo: estudiantes que no han tenido asistencia en los últimos 7 días
        seven_days_ago = today - timedelta(days=7)
        students_without_attendance = (
            db.query(Students.id)
            .outerjoin(Attendance, Attendance.student_id == Students.id)
            .filter(
                Students.status == "Activo",
                ~Attendance.id.isnot(None)  # Esto es solo un ejemplo
            )
            .count()
        )
        pending_alerts = students_without_attendance  

        
        
        return {
            # Cards principales
            "total_students": total_students,
            "students_growth": students_growth,
            "attendance_today": attendance_percentage,
            "attendance_change": attendance_change,
            "present_today": present_today,
            "active_groups": active_groups,
            "different_courses": total_courses,
            "pending_alerts": pending_alerts,
            "total_today": total_today,
            "attendance_yesterday": attendance_yesterday_percentage
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
    
    def get_weekly_attendance(
        self,
        db,
        week_offset=0
    ):

        today = date.today()

        monday = today - timedelta(days=today.weekday())

        monday = monday - timedelta(weeks=week_offset)

        sunday = monday + timedelta(days=6)

        


        records = (

            db.query(Attendance)

            .filter(
                Attendance.date >= monday,
                Attendance.date <= sunday
            )

            .all()

        )

        grouped = {}

        for record in records:

            key = record.date

            if key not in grouped:

                grouped[key] = {

                    "total":0,
                    "present":0

                }

            grouped[key]["total"] += 1

            if record.status in [

                "Asistencia",
                "Retardo"

            ]:

                grouped[key]["present"] += 1

        result = []

        current = monday

        while current <= sunday:

            if current in grouped:

                total = grouped[current]["total"]

                present = grouped[current]["present"]

                percentage = round(

                    present / total * 100,

                    2

                )

            else:

                percentage = 0

            result.append({

                "date": str(current),

                "attendance": percentage

            })

            current += timedelta(days=1)

        return result

            


            
            