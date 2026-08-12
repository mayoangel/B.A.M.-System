from sqlalchemy import Column, Integer, Date, String
from app.core.database import Base

class NonWorkingDays(Base):
    __tablename__ = "non_working_days"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, unique=True)
    description = Column(String(150), nullable=False)