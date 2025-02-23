from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models.lesson import Lesson
from api.configs.loggers import user_logger
from api.schemas.lesson import SLesson


@connection
async def get_lesson_for_id_util(lesson_id: int, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение студента')
    query = (select(Lesson).where(Lesson.id == lesson_id)
             .options(joinedload(Lesson.files), joinedload(Lesson.homeworks)))
    result = await session.execute(query)
    lesson = result.scalars().first()
    lesson_data = SLesson.from_orm(lesson)
    return {
        "data": lesson_data
    }
