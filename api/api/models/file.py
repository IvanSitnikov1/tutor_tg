from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.models import Lesson, Teacher

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declared_attr

from api.configs.database import Base


class BaseFile(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete='CASCADE'), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

    @declared_attr
    def lesson(cls) -> Mapped["Lesson"]:
        return relationship("Lesson", back_populates=cls.__tablename__)


class File(BaseFile):
    __tablename__ = "files"


class Homework(BaseFile):
    __tablename__ = "homeworks"


class PersonalFile(Base):
    __tablename__ = "personal_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

    author: Mapped['Teacher'] = relationship("Teacher", back_populates='personal_files')


class CompletedHomework(BaseFile):
    __tablename__ = "completed_homeworks"


class CommentToCompletedHomework(BaseFile):
    __tablename__ = "comments_to_completed_homeworks"
