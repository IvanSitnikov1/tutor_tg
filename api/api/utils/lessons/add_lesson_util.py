from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.lesson import Lesson
from api.configs.loggers import user_logger
from api.schemas.lesson import SLessonAdd


@connection
async def add_lesson_util(lesson: SLessonAdd, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение студента')
    new_lesson = Lesson(**lesson.model_dump())
    session.add(new_lesson)
    await session.flush()
    await session.commit()
    await session.refresh(new_lesson)
    return {
        "data": new_lesson
    }
