import os

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.app import settings
from api.configs.database import connection
from api.models import File
from api.schemas.lesson import SDeleteFiles
from api.configs.loggers import logger


@connection
async def delete_list_files_util(files_data: SDeleteFiles, session: AsyncSession):
    logger.info('Получен запрос на удаление нескольких материалов урока')
    stmt = select(File).where(File.id.in_(files_data.files_ids))
    result = await session.execute(stmt)
    files = result.scalars().all()
    if not files:
        logger.error('Файлы не найдены')
        raise HTTPException(status_code=404, detail='Файлы не найдены')

    logger.info('Удаление файлов из базы данных...')
    stmt = delete(File).where(File.id.in_(files_data.files_ids))
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount:
        logger.info('Удаление файлов с сервера...')
        for file in files:
            path = settings.STATIC_PATH + file.file_path
            if os.path.exists(path):
                os.remove(path)

        logger.info('Файлы лекции успешно удалены')
        return {
            "detail": "Файлы лекции успешно удалены"
        }
    else:
        logger.error('Не удалось удалить файлы лекции')
        raise HTTPException(status_code=400, detail="Не удалось удалить файлы лекции")
