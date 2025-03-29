from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import CommentToCompletedHomework
from api.schemas.lesson import SFileAdd
from api.configs.loggers import logger


@connection
async def add_comment_to_completed_homework_util(file: SFileAdd, session: AsyncSession):
    logger.info('Получен запрос на добавление комментария к выполненному домашнему заданию')
    new_file = CommentToCompletedHomework(**file.model_dump())
    session.add(new_file)

    try:
        await session.commit()
        logger.info(f'Файл добавлен успешно: {file.file_path}')
        return {
            "detail": "Файл добавлен успешно"
        }
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при добавлении файла в базу данных: {e}')
        raise HTTPException(status_code=500, detail="Ошибка при добавлении файла")
