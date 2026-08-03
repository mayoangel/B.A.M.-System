from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Matrícula generada por el sistema (ver StudentService._generate_matricula);
    # nunca se acepta un valor de matrícula proveniente del cliente.
    id_student = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    surename = Column(String(100), nullable=True)
    # Los alumnos son menores de edad: no tienen credenciales propias ni datos
    # de contacto/dirección independientes. Esa información vive únicamente
    # en su tutor (Parents), referenciado por `id_parent`.
    date_of_birth = Column(Date, nullable=False)
    status = Column(String(50), nullable=False, default="Activo")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    id_parent = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)

    parent = relationship("Parents", back_populates="students")
    attendance = relationship("Attendance", back_populates="students", cascade="all, delete-orphan")
    student_tutor = relationship("StudentTutor", back_populates="students", cascade="all, delete-orphan")
    courses = relationship("Courses", secondary="student_courses", back_populates="students")
    student_courses_rel = relationship("StudentCourses", back_populates="student", cascade="all, delete-orphan")
    biometric_information = relationship("BiometricInformation", back_populates="student", cascade="all, delete-orphan")
