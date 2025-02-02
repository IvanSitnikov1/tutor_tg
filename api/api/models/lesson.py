from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.configs.database import Base

if TYPE_CHECKING:
    from api.models.user import Student, Homework


class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete='CASCADE'), nullable=False)

    student: Mapped["Student"] = relationship("Student", back_populates="lessons")
    homeworks: Mapped[list["Homework"]] = relationship('Homework', back_populates='lesson')
