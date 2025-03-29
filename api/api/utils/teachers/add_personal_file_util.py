from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import PersonalFile
from api.schemas.teacher import SPersonalFileAdd
from api.configs.loggers import logger


@connection
async def add_personal_file_util(
        file_data: SPersonalFileAdd,
        session: AsyncSession,
):
    logger.info('Получен запрос на добавление личного файла для учителя')
    file = PersonalFile(**file_data.model_dump())
    session.add(file)
    try:
        await session.flush()
        await session.commit()
        await session.refresh(file)
        logger.info(f'Файл добавлен успешно: {file.file_path}')

        return {
            'data': file,
            'detail': 'Файл успешно добавлен',
        }
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при добавлении файла в базу данных: {e}')
        raise HTTPException(status_code=500, detail="Ошибка при добавлении файла")
