import os

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.app import settings
from api.configs.database import connection
from api.models import File, Homework


@connection
async def delete_all_files_by_type_util(lesson_id: int, file_type: str, session: AsyncSession):
    if file_type == 'files':
        table = File
    else:
        table = Homework

    query = select(table).where(table.lesson_id == lesson_id)
    result = await session.execute(query)
    files = result.scalars().all()

    for file in files:
        path = settings.STATIC_PATH + file.file_path
        if os.path.exists(path):
            os.remove(path)

    stmt = delete(table).where(table.lesson_id == lesson_id)
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount:
        return {
            "detail": "Файлы лекции успешно удалены"
        }
    raise HTTPException(status_code=400, detail="Не удалось удалить файлы лекции")
