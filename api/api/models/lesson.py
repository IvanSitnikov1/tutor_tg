from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.models import Student, Teacher, Homework, File, CompletedHomework, CommentToCompletedHomework

from sqlalchemy import Integer, String, ForeignKey, Boolean, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.configs.database import Base


class Lesson(Base):
    """
    Модель урока в системе обучения.

    Attributes:
        id (int): Уникальный идентификатор урока (первичный ключ)
        name (str): Название урока
        is_done (bool): Статус завершения урока (по умолчанию False)
        date (Date): Дата урока (по умолчанию текущая дата)
        student_id (int): ID студента (tg id, каскадное удаление)
        author_id (int): ID преподавателя (tg id, каскадное удаление)
        student (Student): Связанный объект студента
        author (Teacher): Связанный объект преподавателя
        files (List[File]): Прикрепленные файлы урока
        homeworks (List[Homework]): Домашние задания к уроку
        completed_homeworks (List[CompletedHomework]): Выполненные домашние задания
        comments_to_completed_homeworks (List[CommentToCompletedHomework]): Комментарии к выполненным заданиям
    """

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
