from sqlalchemy import Column, Integer, String, DateTime, ForeignKey 
from sqlalchemy.orm import relationship
from app.core.database import Base

class Employees(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_employee = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    surename = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    status = Column(String(100), nullable=False)
    dir_street = Column(String(100), nullable=False)
    dir_col = Column(String(100), nullable=False)
    dir_num = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

    role = relationship("Role", back_populates="employees")
    attendance = relationship("Attendance", back_populates="employees")
    student_tutor = relationship("StudentTutor", back_populates="employees")
    employee_course = relationship("EmployeeCourse", back_populates="employees")
    reports = relationship("Reports", back_populates="employee")