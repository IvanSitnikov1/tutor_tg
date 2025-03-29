from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models import Student
from api.configs.loggers import logger


@connection
async def get_student_by_id_util(student_id: int, session: AsyncSession):
    logger.info('Получен запрос на получение информации о студенте')
    query = select(Student).where(Student.id == student_id).options(joinedload(Student.lessons))
    result = await session.execute(query)
    student = result.scalars().first()

    if student:
        logger.info('Данные студента получены успешно')
        return {
            'data': student,
            'detail': 'Данные студента получены успешно',
        }
    else:
        logger.error('Не удалось получить данные студента')
        raise HTTPException(status_code=404, detail="Не удалось получить данные студента")
