import os

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import PersonalFile
from api.schemas.lesson import SDeleteFiles


@connection
async def delete_list_personal_files_util(personal_files_data: SDeleteFiles, session: AsyncSession):
    stmt = select(PersonalFile).where(PersonalFile.id.in_(personal_files_data.files_ids))
    result = await session.execute(stmt)
    files = result.scalars().all()

    for file in files:
        path = f'/home/ivan/Projects/tutor_tg/static{file.file_path}'
        if os.path.exists(path):
            os.remove(path)

    stmt = delete(PersonalFile).where(PersonalFile.id.in_(personal_files_data.files_ids))
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount:
        return {
            "data": "Персональные файлы пользователя успешно удалены"
        }
