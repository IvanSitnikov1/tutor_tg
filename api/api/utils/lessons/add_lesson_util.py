from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.lesson import Lesson
from api.schemas.lesson import SLessonAdd


@connection
async def add_lesson_util(lesson: SLessonAdd, session: AsyncSession):
    new_lesson = Lesson(**lesson.model_dump())
    session.add(new_lesson)

    try:
        await session.commit()
        return {
            "detail": "Урок добавлен успешно"
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Ошибка при добавлении урока")
