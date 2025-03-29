from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.lesson import Lesson
from api.configs.loggers import logger


@connection
async def update_lesson_date_util(lesson_id: int, new_date: str, session: AsyncSession):
    logger.info('Получен запрос на изменение даты урока')
    lesson = await session.get(Lesson, lesson_id)
    try:
        lesson.date = datetime.strptime(new_date, '%d-%m-%Y').date()
    except ValueError:
        logger.error('Переданный формат даты не соответствует ожидаемому')
        raise HTTPException(status_code=400, detail="Переданный формат даты не соответствует ожидаемому - %d-%m-%Y")

    try:
        await session.commit()
        logger.info('Дата лекции обновлена успешно')
        return {
            "data": new_date,
            "detail": "Дата лекции обновлена успешно",
        }
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при обновлении даты лекции: {e}')
        raise HTTPException(status_code=500, detail="Ошибка при обновлении даты лекции")
