from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, BigInteger

from api.configs.database import Base

if TYPE_CHECKING:
    from api.models.lesson import Lesson


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # Для определения типа ('teacher' или 'student')

    __mapper_args__ = {
        "polymorphic_identity": "user",  # Определение базового типа
        "polymorphic_on": type,  # Дискиминационный тип
    }


class Teacher(User):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)

    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="teacher",
        foreign_keys="Student.teacher_id",
    )

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }


class Student(User):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete='CASCADE'), nullable=False)

    lessons: Mapped[list["Lesson"]] = relationship('Lesson', back_populates='student')
    teacher: Mapped[int] = relationship(
        'Teacher',
        back_populates='students',
        foreign_keys=[teacher_id],
    )

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }
