import os

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import PersonalFile
from api.schemas.lesson import SDeleteFiles
from api.configs.loggers import logger


@connection
async def delete_list_personal_files_util(personal_files_data: SDeleteFiles, session: AsyncSession):
    logger.info('Получен запрос на удаление нескольких личных файлов учителя')
    stmt = select(PersonalFile).where(PersonalFile.id.in_(personal_files_data.files_ids))
    result = await session.execute(stmt)
    files = result.scalars().all()
    if not files:
        logger.error('Файлы не найдены')
        raise HTTPException(status_code=404, detail='Файлы не найдены')

    logger.info('Удаление файлов из базы данных...')
    stmt = delete(PersonalFile).where(PersonalFile.id.in_(personal_files_data.files_ids))
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount:
        logger.info('Удаление файлов с сервера...')
        for file in files:
            path = f'/home/ivan/Projects/tutor_tg/static{file.file_path}'
            if os.path.exists(path):
                os.remove(path)

        logger.info('Выбранные персональные файлы успешно удалены')
        return {
            "detail": "Выбранные персональные файлы успешно удалены"
        }
    else:
        logger.error('Не удалось удалить выбранные персональные файлы')
        raise HTTPException(status_code=400, detail="Не удалось удалить выбранные персональные файлы")
