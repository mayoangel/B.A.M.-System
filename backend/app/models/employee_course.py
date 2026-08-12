from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmployeeCourse(Base):
    __tablename__ = "employee_course"
    employee_id = Column(Integer, ForeignKey("employees.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    employees = relationship("Employees", back_populates="employee_course")
    courses = relationship("Courses", back_populates="employee_course")