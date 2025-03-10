import os

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.app import settings
from api.configs.database import connection
from api.models.lesson import Lesson


@connection
async def delete_lesson_util(lesson_id: int, session: AsyncSession):
    stmt = select(Lesson).where(Lesson.id == lesson_id).options(
        joinedload(Lesson.files),
        joinedload(Lesson.homeworks),
        joinedload(Lesson.completed_homeworks),
        joinedload(Lesson.comments_to_completed_homeworks),
    )
    result = await session.execute(stmt)
    lesson = result.scalars().first()

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

    stmt = delete(Lesson).where(Lesson.id == lesson_id)
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount:
        return {
            "detail": "Урок удален успешно"
        }
    raise HTTPException(status_code=400, detail="Не удалось удалить урок")
