from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import Homework
from api.schemas.lesson import SDeleteFiles


@connection
async def delete_list_homeworks_util(homeworks_data: SDeleteFiles, session: AsyncSession):
    stmt = delete(Homework).where(Homework.id.in_(homeworks_data.files_ids))
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount:
        return {
            "data": "Домашние задания успешно удалены"
        }
