from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.reports_repository import ReportsRepository
from app.models.reports import Reports

class ReportService:
    def __init__(self, db: Session):
        self.repository = ReportsRepository(db)

    def register_report(self, report_data: dict) -> Reports:
        if not report_data.get("name"):
            raise ValueError("El nombre del reporte es obligatorio.")
        if not report_data.get("employee_id"):
            raise ValueError("Se requiere especificar el ID del empleado que generó el reporte.")

        if not report_data.get("generation_date"):
            report_data["generation_date"] = datetime.now()

        existing = self.repository.get_report_by_name(report_data.get("name"))
        if existing:
            raise ValueError("Ya existe un reporte registrado con ese nombre.")
            
        return self.repository.registerReport(report_data)
    
    def list_all_reports(self) -> list[Reports]:
        return self.repository.getAllReports()

    def get_reports_by_date(self, date_str: str) -> list[Reports]:
        if not date_str:
            raise ValueError("La fecha de búsqueda es obligatoria.")
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Utilice el formato YYYY-MM-DD.")
            
        return self.repository.getReportsByDate(parsed_date)

    def get_report_by_name(self, report_name: str) -> Reports:
        report = self.repository.get_report_by_name(report_name)
        if not report:
            raise ValueError(f"El reporte '{report_name}' no fue encontrado.")
        return report

    def update_report(self, report_name: str, new_data: dict) -> bool:
        updated = self.repository.update_report(report_name, new_data)
        if not updated:
            raise ValueError(f"No se pudo actualizar: El reporte '{report_name}' no existe.")
        return True

    def delete_report(self, report_name: str) -> bool:
        deleted = self.repository.delete_report(report_name)
        if not deleted:
            raise ValueError(f"No se pudo eliminar: El reporte '{report_name}' no existe.")
        return True