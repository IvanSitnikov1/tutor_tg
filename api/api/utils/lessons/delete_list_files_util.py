import os

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.app import settings
from api.configs.database import connection
from api.models import File
from api.schemas.lesson import SDeleteFiles


@connection
async def delete_list_files_util(files_data: SDeleteFiles, session: AsyncSession):
    stmt = select(File).where(File.id.in_(files_data.files_ids))
    result = await session.execute(stmt)
    files = result.scalars().all()

    for file in files:
        path = settings.STATIC_PATH + file.file_path
        if os.path.exists(path):
            os.remove(path)

    stmt = delete(File).where(File.id.in_(files_data.files_ids))
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount:
        return {
            "detail": "Файлы лекции успешно удалены"
        }
    raise HTTPException(status_code=400, detail="Не удалось удалить файлы лекции")
