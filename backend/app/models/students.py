from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Students(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_student = Column(String(50), nullable=False, unique=True)  
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    surename = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    dir_col = Column(String(100), nullable=False)
    dir_street = Column(String(100), nullable=False)
    dir_num = Column(String(100), nullable=False)   
    status = Column(String(50), nullable=False, default="Activo")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    id_parent = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)

    parent = relationship("Parents", back_populates="students")
    attendance = relationship("Attendance", back_populates="students", cascade="all, delete-orphan")
    student_tutor = relationship("StudentTutor", back_populates="students", cascade="all, delete-orphan")
    courses = relationship("Courses", secondary="student_courses", back_populates="students")
    student_courses_rel = relationship("StudentCourses", back_populates="student", cascade="all, delete-orphan")
    biometric_information = relationship("BiometricInformation", back_populates="student", cascade="all, delete-orphan")