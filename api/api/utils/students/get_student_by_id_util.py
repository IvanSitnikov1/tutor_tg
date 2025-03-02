from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models import Student
from api.configs.loggers import user_logger


@connection
async def get_student_by_id_util(student_id: int, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение студента')
    query = select(Student).where(Student.id == student_id).options(joinedload(Student.lessons))
    result = await session.execute(query)
    student = result.scalars().first()

    if student:
        return {
            'data': student,
            'detail': 'Данные студента получены успешно',
        }
    raise HTTPException(status_code=400, detail="Не удалось получить данные студента")
