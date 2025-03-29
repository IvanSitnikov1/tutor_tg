from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models import Lesson
from api.configs.loggers import logger


@connection
async def get_lesson_for_id_util(lesson_id: int, session: AsyncSession):
    logger.info('Получен запрос на получение информации о уроке')
    query = (select(Lesson).where(Lesson.id == lesson_id).options(
        joinedload(Lesson.files),
        joinedload(Lesson.homeworks),
        joinedload(Lesson.completed_homeworks),
        joinedload(Lesson.comments_to_completed_homeworks),
    ))
    result = await session.execute(query)
    lesson = result.unique().scalar_one_or_none()

    if lesson:
        logger.info('Данные урока получены успешно')
        return {
            'data': lesson,
            'detail': 'Данные урока получены успешно',
        }
    else:
        logger.error('Не удалось получить данные урока')
        raise HTTPException(status_code=404, detail='Не удалось получить данные урока')
