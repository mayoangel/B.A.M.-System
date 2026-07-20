from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.non_working_days_repository import NonWorkingDaysRepository

class NonWorkingDaysService:
    def __init__(self, db: Session):
        self.repository = NonWorkingDaysRepository(db)

    def list_all_days(self):
        return self.repository.get_all()

    def add_non_working_day(self, date_str: str, description: str):
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Utilice YYYY-MM-DD.")


        existing = self.repository.get_by_date(parsed_date)
        if existing:
            raise ValueError(f"La fecha {date_str} ya está registrada como día inhábil.")

        day_data = {
            "date": parsed_date,
            "description": description
        }
        return self.repository.create(day_data)

    def delete_non_working_day(self, id: int):
        success = self.repository.delete(id)
        if not success:
            raise ValueError("El día inhábil especificado no existe.")
        return {"message": "Día inhábil eliminado correctamente."}