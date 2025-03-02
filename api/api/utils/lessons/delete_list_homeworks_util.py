import os

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import Homework
from api.schemas.lesson import SDeleteFiles


@connection
async def delete_list_homeworks_util(homeworks_data: SDeleteFiles, session: AsyncSession):
    stmt = select(Homework).where(Homework.id.in_(homeworks_data.files_ids))
    result = await session.execute(stmt)
    files = result.scalars().all()

    for file in files:
        path = f'/home/ivan/Projects/tutor_tg/static{file.file_path}'
        if os.path.exists(path):
            os.remove(path)

    stmt = delete(Homework).where(Homework.id.in_(homeworks_data.files_ids))
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount:
        return {
            "detail": "Домашние задания успешно удалены"
        }
    raise HTTPException(status_code=400, detail="Не удалось удалить домашние задания")
