from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class StudentCourses(Base):
    __tablename__ = "student_courses"
 
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)

    student = relationship("Students", back_populates="student_courses_rel")
    course = relationship("Courses", back_populates="student_courses_rel")