from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import Student


@connection
async def get_students_list_ids_util(session: AsyncSession):
    query = select(Student.id)
    result = await session.execute(query)
    return {
        "data": result.scalars().all(),
        "detail": "Список id студентов получен успешно",
    }
