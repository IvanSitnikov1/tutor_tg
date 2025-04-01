from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.models import Lesson, Teacher

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declared_attr

from api.configs.database import Base


class BaseFile(Base):
    """
    Абстрактная базовая модель для файловых сущностей.

    Attributes:
        id (int): Уникальный идентификатор (primary key)
        lesson_id (int): ID урока (внешний ключ, каскадное удаление)
        file_path (str): Путь к файлу в хранилище
        lesson (Lesson): Связанный объект урока
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete='CASCADE'), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

    @declared_attr
    def lesson(cls) -> Mapped["Lesson"]:
        return relationship("Lesson", back_populates=cls.__tablename__)


class File(BaseFile):
    """
    Модель материала урока.

    Attributes:
        Наследует все атрибуты от BaseFile
    """

    __tablename__ = "files"


class Homework(BaseFile):
    """
    Модель домашнего задания.

    Attributes:
        Наследует все атрибуты от BaseFile
    """

    __tablename__ = "homeworks"


class PersonalFile(Base):
    """
    Модель личных файлов преподавателя.

    Attributes:
        id (int): Уникальный идентификатор (primary key)
        author_id (int): ID преподавателя (внешний ключ)
        file_path (str): Путь к файлу в хранилище
        author (Teacher): Связанный объект преподавателя
    """

    __tablename__ = "personal_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

    author: Mapped['Teacher'] = relationship("Teacher", back_populates='personal_files')


class CompletedHomework(BaseFile):
    """
    Модель выполненного домашнего задания.

    Attributes:
        Наследует все атрибуты от BaseFile
    """

    __tablename__ = "completed_homeworks"


class CommentToCompletedHomework(BaseFile):
    """
    Модель комментария к домашнему заданию.

    Attributes:
        Наследует все атрибуты от BaseFile
    """
    __tablename__ = "comments_to_completed_homeworks"
