from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class BiometricInformation(Base):
    __tablename__ = "biometric_information"
    id = Column(Integer, primary_key=True, autoincrement=True)
    face_vector = Column(Text, nullable=False)
    encryption_hash = Column(String(255), nullable=False)
    enrollment_date = Column(DateTime, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, unique=True)
    student = relationship("Students", back_populates="biometric_information")