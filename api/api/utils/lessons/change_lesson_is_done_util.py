from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import Lesson
from api.configs.loggers import logger


@connection
async def change_lesson_is_done_util(lesson_id: int, session: AsyncSession):
    logger.info('Получен запрос на изменение состояния урока (выполнен/не выполнен)')
    lesson = await session.get(Lesson, lesson_id)

    if lesson:
        lesson.is_done = not lesson.is_done
        try:
            await session.commit()
            logger.info(f'Состояние урока изменено с {str(not lesson.is_done)} на {str(lesson.is_done)}')
            return {
                "data": lesson.is_done,
                "detail": "Состояние урока изменено успешно"
            }
        except SQLAlchemyError as e:
            logger.error(f'Ошибка при изменении состояния урока: {e}')
            raise HTTPException(status_code=500, detail="Ошибка при изменении состояния урока")
    else:
        logger.error('Запрашиваемого урока не существует')
        raise HTTPException(status_code=400, detail='Запрашиваемого урока не существует')
