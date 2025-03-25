from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.lesson import Lesson


@connection
async def update_lesson_date_util(lesson_id: int, new_date: str, session: AsyncSession):
    lesson = await session.get(Lesson, lesson_id)
    lesson.date = datetime.strptime(new_date, '%d-%m-%Y').date()

    try:
        await session.commit()
        return {
            "data": new_date,
            "detail": "Дата лекции обновлена успешно",
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении даты лекции")
