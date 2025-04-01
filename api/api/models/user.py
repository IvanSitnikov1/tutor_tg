from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.models import Lesson, PersonalFile

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, BigInteger

from api.configs.database import Base


class User(Base):
    """
    Базовый класс пользователя системы.

    Использует полиморфную загрузку (inheritance) через поле type.
    Является родительским классом для Teacher и Student.

    Attributes:
        id (int): Уникальный идентификатор пользователя (tg id)
        username (str): Уникальное имя пользователя
        type (str): Тип пользователя (дискриминатор для наследования)
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "user",  # Определение базового типа
        "polymorphic_on": type,  # Дискиминационный тип
    }


class Teacher(User):
    """
    Модель преподавателя в системе.

    Наследуется от User, добавляет связи с уроками, студентами и файлами.

    Attributes:
        id (int): Ссылка на id в таблице users (первичный ключ, каскадное удаление)
        lessons (list[Lesson]): Список уроков, созданных преподавателем
        students (list[Student]): Список студентов преподавателя
        personal_files (list[PersonalFile]): Личные файлы преподавателя
    """

    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)

    lessons: Mapped[list["Lesson"]] = relationship('Lesson', back_populates='author')
    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="teacher",
        foreign_keys="Student.teacher_id",
    )
    personal_files: Mapped[list["PersonalFile"]] = relationship(
        "PersonalFile", back_populates="author")

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }


class Student(User):
    """
    Модель студента в системе.

    Наследуется от User, содержит ссылку на преподавателя.

    Attributes:
        id (int): Ссылка на id в таблице users (первичный ключ, каскадное удаление)
        teacher_id (int): ID преподавателя студента (вторичный ключ, каскадное удаление)
        teacher (Teacher): Объект преподавателя
        lessons (list[Lesson]): Список уроков студента
    """

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete='CASCADE'),
        primary_key=True,
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete='CASCADE'),
        nullable=False,
    )

    lessons: Mapped[list["Lesson"]] = relationship('Lesson', back_populates='student')
    teacher: Mapped['Teacher'] = relationship(
        'Teacher',
        back_populates='students',
        foreign_keys=[teacher_id],
    )

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }
