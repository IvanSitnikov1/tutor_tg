import os

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import Homework
from api.schemas.lesson import SDeleteFiles
from api.configs.loggers import logger


@connection
async def delete_list_homeworks_util(homeworks_data: SDeleteFiles, session: AsyncSession):
    logger.info('Получен запрос на удаление нескольких домашних заданий урока')
    stmt = select(Homework).where(Homework.id.in_(homeworks_data.files_ids))
    result = await session.execute(stmt)
    files = result.scalars().all()
    if not files:
        logger.error('Файлы не найдены')
        raise HTTPException(status_code=404, detail='Файлы не найдены')

    logger.info('Удаление файлов из базы данных...')
    stmt = delete(Homework).where(Homework.id.in_(homeworks_data.files_ids))
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount:
        logger.info('Удаление файлов с сервера...')
        for file in files:
            path = f'/home/ivan/Projects/tutor_tg/static{file.file_path}'
            if os.path.exists(path):
                os.remove(path)

        logger.info('Домашние задания успешно удалены')
        return {
            "detail": "Домашние задания успешно удалены"
        }
    else:
        logger.error('Не удалось удалить домашние задания')
        raise HTTPException(status_code=400, detail='Не удалось удалить домашние задания')
