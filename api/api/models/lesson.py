from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.configs.database import Base

if TYPE_CHECKING:
    from api.models import Student, Homework, File


class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete='CASCADE'), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    files: Mapped[list["File"]] = relationship("File", back_populates="lesson")
    homeworks: Mapped[list["Homework"]] = relationship('Homework', back_populates='lesson')
    student: Mapped["Student"] = relationship("Student", back_populates="lessons")
