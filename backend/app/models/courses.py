from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    time_duration = Column(String(50), nullable=False)
    days_of_week = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="Activo")

    pre_register = relationship("PreRegister", back_populates="courses")
    employee_course = relationship("EmployeeCourse", back_populates="courses")
    students = relationship("Students", secondary="student_courses", back_populates="courses")
    attendance = relationship("Attendance", back_populates="course")
    student_courses_rel = relationship("StudentCourses", back_populates="course", cascade="all, delete-orphan")