from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String(50), nullable=False)
    method = Column(String(50), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    students = relationship("Students", back_populates= "attendance")
    employees = relationship("Employees", back_populates= "attendance")
    course = relationship("Courses", back_populates="attendance")