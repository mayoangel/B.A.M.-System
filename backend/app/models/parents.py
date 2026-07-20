from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Parents(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    surename = Column(String(100), nullable=True)
    phone = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    students = relationship("Students", back_populates="parent")