from app.repositories.dashboardRepository import DashboardRepository

##### AGREGADO PARA EL DASBOARD ######
class DashboardService:

    def __init__(self):

        self.repository = DashboardRepository()


    def get_summary(self, db):

        return self.repository.get_summary(db)


    def get_courses_distribution(self, db):

        return self.repository.get_courses_distribution(db)
    

    ####

    def get_kpis(self, db):

        return self.repository.get_kpis(db)
    
    ######
    #####
    def get_history(
        self,
        db,
        student_id=None,
        course_id=None,
        start_date=None,
        end_date=None
    ):

        return self.repository.get_history(
            db,
            student_id,
            course_id,
            start_date,
            end_date
        )
    
    def get_weekly_attendance(
        self,
        db,
        week_offset=0
    ):

        return self.repository.get_weekly_attendance(
            db,
            week_offset
        )