from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import User


@connection
async def get_students_list_tg_id_util(session: AsyncSession):
    query = select(User.tg_id).where(User.type == 'student')
    result = await session.execute(query)
    return {
        "data": result.scalars().all()
    }
