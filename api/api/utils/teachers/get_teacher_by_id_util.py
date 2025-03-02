from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models import Teacher


@connection
async def get_teacher_by_id_util(teacher_id, session: AsyncSession):
    query = (select(Teacher).where(Teacher.id == teacher_id)
            .options(joinedload(Teacher.students))
            .options(joinedload(Teacher.personal_files))
            .options(joinedload(Teacher.lessons))
             )
    result = await session.execute(query)
    teacher = result.scalars().first()
    if teacher:
        return {
            'data': teacher,
            'detail': 'Данные учителя получены успешно',
        }
    raise HTTPException(status_code=400, detail="Не удалось получить данные учителя")
