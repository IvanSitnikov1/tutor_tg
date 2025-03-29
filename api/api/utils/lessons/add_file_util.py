from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.file import File
from api.schemas.lesson import SFileAdd
from api.configs.loggers import logger


@connection
async def add_file_util(file: SFileAdd, session: AsyncSession):
    logger.info('Получен запрос на добавление материала к уроку')
    new_file = File(**file.model_dump())
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
