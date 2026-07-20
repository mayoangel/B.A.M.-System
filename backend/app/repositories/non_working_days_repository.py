from sqlalchemy.orm import Session
from datetime import date
from app.models.non_working_days import NonWorkingDays

class NonWorkingDaysRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(NonWorkingDays).order_by(NonWorkingDays.date.asc()).all()

    def get_by_date(self, target_date: date):
        return self.db.query(NonWorkingDays).filter(NonWorkingDays.date == target_date).first()

    def get_by_id(self, id: int):
        return self.db.query(NonWorkingDays).filter(NonWorkingDays.id == id).first()

    def create(self, day_data: dict) -> NonWorkingDays:
        db_day = NonWorkingDays(**day_data)
        self.db.add(db_day)
        self.db.commit()
        self.db.refresh(db_day)
        return db_day

    def delete(self, id: int) -> bool:
        db_day = self.get_by_id(id)
        if not db_day:
            return False
        self.db.delete(db_day)
        self.db.commit()
        return True