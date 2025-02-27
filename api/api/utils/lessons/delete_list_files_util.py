import os

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import File
from api.schemas.lesson import SDeleteFiles


@connection
async def delete_list_files_util(files_data: SDeleteFiles, session: AsyncSession):
    stmt = select(File).where(File.id.in_(files_data.files_ids))
    result = await session.execute(stmt)
    files = result.scalars().all()

    for file in files:
        os.remove(f'/home/ivan/Projects/tutor_tg/static{file.file_path}')

    stmt = delete(File).where(File.id.in_(files_data.files_ids))
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount:
        return {
            "data": "Файлы лекции успешно удалены"
        }
