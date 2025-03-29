from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.lesson import Lesson
from api.schemas.lesson import SLessonAdd
from api.configs.loggers import logger


@connection
async def add_lesson_util(lesson: SLessonAdd, session: AsyncSession):
    logger.info('Получен запрос на добавление урока')
    new_lesson = Lesson(**lesson.model_dump())
    session.add(new_lesson)

    try:
        await session.flush()
        await session.commit()
        await session.refresh(new_lesson)
        logger.info(f'Урок {lesson.name} добавлен успешно')

        return {
            "data": new_lesson,
            "detail": "Урок добавлен успешно",
        }
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при добавлении урока в базу данных: {e}')
        raise HTTPException(status_code=500, detail="Ошибка при добавлении урока")
