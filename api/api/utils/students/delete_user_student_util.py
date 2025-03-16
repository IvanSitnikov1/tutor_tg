import os

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from api.configs.app import settings
from api.configs.database import connection
from api.models import Student, Lesson, User


@connection
async def delete_user_student_util(student_id: int, session: AsyncSession):
    query = select(Student).where(Student.id == student_id).options(
        selectinload(Student.lessons).options(
            selectinload(Lesson.files),
            selectinload(Lesson.homeworks),
            selectinload(Lesson.completed_homeworks),
            selectinload(Lesson.comments_to_completed_homeworks),
        ),
    )

    result = await session.execute(query)
    student = result.scalar_one_or_none()

    if student:
        for lesson in student.lessons:
            for file_list in [
                lesson.files,
                lesson.homeworks,
                lesson.completed_homeworks,
                lesson.comments_to_completed_homeworks
            ]:
                for file in file_list:
                    file_path = settings.STATIC_PATH + file.file_path
                    if os.path.exists(file_path):
                        os.remove(file_path)

        stmt = delete(User).where(User.id == student_id)
        await session.execute(stmt)

        try:
            await session.commit()
        except SQLAlchemyError:
            raise HTTPException(status_code=400, detail="Ошибка при удалении ученика")

        return {
            'detail': 'Ученик удален успешно'
        }
    else:
        return {
            'detail': 'Запрашиваемого пользователя не существует',
        }
