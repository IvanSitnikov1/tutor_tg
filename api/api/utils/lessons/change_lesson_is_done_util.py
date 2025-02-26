from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import Lesson


@connection
async def change_lesson_is_done_util(lesson_id: int, session: AsyncSession):
    lesson = await session.get(Lesson, lesson_id)  # Получаем запись

    if lesson:
        lesson.is_done = not lesson.is_done  # Меняем значение на противоположное
        await session.commit()
        return {
            "data": lesson.is_done
        }
