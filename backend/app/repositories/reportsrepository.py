from sqlalchemy.orm import Session
from app.models.reports import Reports

class ReportsRepository:
    def __init__ (self,db:Session):
        self.db = db

    #crear reporte
    def registerReport(self, report_data: dict) -> Reports:
        db_report = Reports(**report_data)
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report
    
    # Traer todos los reportes ordenados por fecha de generación
    def getAllReports(self) -> list[Reports]:
        return self.db.query(Reports).order_by(Reports.generation_date.desc()).all()

    # Buscar reportes filtrados por una fecha específica
    from datetime import date
    def getReportsByDate(self, target_date: date) -> list[Reports]:
        return self.db.query(Reports).filter(
            self.db.func.date(Reports.generation_date) == target_date
        ).order_by(Reports.generation_date.desc()).all()

    #buscar roporte por nombre
    def get_report_by_name(self, reportName: str) -> Reports:
        return self.db.query(Reports).filter(Reports.name == reportName).first()

    #actualizar roporte
    def update_report(self, reportName: str, new_data: dict) -> bool:
        db_report = self.get_report_by_name(reportName)
        if db_report:
            for key, value in new_data.items():
                setattr(db_report, key, value)
            self.db.commit()
            return True
        return False

    #eliminar roporte
    def delete_report(self, reportName: str) -> bool:
        db_report = self.get_report_by_name(reportName)
        if db_report:
            self.db.delete(db_report)
            self.db.commit()
            return True
        return False