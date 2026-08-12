from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PreRegister(Base):
    __tablename__ = "pre_register"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    surename = Column(String(100), nullable=True)
    email = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    courses = relationship("Courses", back_populates = "pre_register")