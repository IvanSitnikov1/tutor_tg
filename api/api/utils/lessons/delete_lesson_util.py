from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.lesson import Lesson
from api.configs.loggers import user_logger


@connection
async def delete_lesson_util(lesson_id: int, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение студента')
    stmt = delete(Lesson).where(Lesson.id == lesson_id)
    await session.execute(stmt)
    await session.commit()
    return {
        "data": "lesson deleted"
    }
