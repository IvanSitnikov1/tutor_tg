from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models import Lesson


@connection
async def get_lesson_for_id_util(lesson_id: int, session: AsyncSession):
    query = (select(Lesson).where(Lesson.id == lesson_id).options(
        joinedload(Lesson.files),
        joinedload(Lesson.homeworks),
        joinedload(Lesson.completed_homeworks),
        joinedload(Lesson.comments_to_completed_homeworks),
    ))
    result = await session.execute(query)
    lesson = result.scalars().first()

    if lesson:
        return {
            'data': lesson,
            'detail': 'Данные урока получены успешно',
        }
    raise HTTPException(status_code=400, detail="Не удалось получить данные урока")
