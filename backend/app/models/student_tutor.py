from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class StudentTutor(Base):
    __tablename__ = "student_tutor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    students = relationship("Students", back_populates="student_tutor")
    employees = relationship("Employees", back_populates="student_tutor")