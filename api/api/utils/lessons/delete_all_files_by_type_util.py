import os

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.app import settings
from api.configs.database import connection
from api.models import File, Homework
from api.configs.loggers import logger


@connection
async def delete_all_files_by_type_util(lesson_id: int, file_type: str, session: AsyncSession):
    logger.info(f'Получен запрос на удалелние всех файлов типа - {file_type} из урока')
    if file_type == 'files':
        table = File
    else:
        table = Homework

    query = select(table).where(table.lesson_id == lesson_id)
    result = await session.execute(query)
    files = result.scalars().all()
    if not files:
        logger.error('Файлы не найдены')
        raise HTTPException(status_code=404, detail='Файлы не найдены')

    logger.info('Удаление файлов из базы данных...')
    stmt = delete(table).where(table.lesson_id == lesson_id)
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
        raise HTTPException(status_code=400, detail='Не удалось удалить файлы лекции')
