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
    # El tutor es ahora el único titular de credenciales, contacto y
    # dirección dentro de la relación alumno-tutor (los alumnos son
    # menores de edad y no tienen estos datos propios).
    password = Column(String(255), nullable=False)
    dir_street = Column(String(150), nullable=False)
    dir_col = Column(String(100), nullable=False)
    dir_num = Column(String(50), nullable=False)

    students = relationship("Students", back_populates="parent")
