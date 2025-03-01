from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models import Student


@connection
async def get_student_for_tg_id_util(student_tg_id, session: AsyncSession):
    query = (select(Student).where(Student.tg_id == student_tg_id)
             .options(joinedload(Student.lessons)))
    result = await session.execute(query)
    student = result.scalars().first()
    return {"data": student}
