from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.models import Student, Teacher, Homework, File, CompletedHomework, CommentToCompletedHomework

from sqlalchemy import Integer, String, ForeignKey, Boolean, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.configs.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    date: Mapped[Date] = mapped_column(Date, server_default=func.current_date(), nullable=False)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete='CASCADE'),
        nullable=False,
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete='CASCADE'),
        nullable=False,
    )

    student: Mapped["Student"] = relationship("Student", back_populates="lessons")
    author: Mapped["Teacher"] = relationship("Teacher", back_populates="lessons")
    files: Mapped[list["File"]] = relationship("File", back_populates="lesson")
    homeworks: Mapped[list["Homework"]] = relationship('Homework', back_populates='lesson')
    completed_homeworks: Mapped[list["CompletedHomework"]] = relationship(
        "CompletedHomework",
        back_populates="lesson",
    )
    comments_to_completed_homeworks: Mapped[list["CommentToCompletedHomework"]] = relationship(
        "CommentToCompletedHomework",
        back_populates="lesson",
    )
