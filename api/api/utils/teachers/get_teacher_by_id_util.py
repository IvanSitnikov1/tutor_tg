from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models import Teacher
from api.configs.loggers import logger


@connection
async def get_teacher_by_id_util(teacher_id, session: AsyncSession):
    logger.info('Получен запрос на получение информации о учителе')
    query = (select(Teacher).where(Teacher.id == teacher_id)
            .options(joinedload(Teacher.students))
            .options(joinedload(Teacher.personal_files))
            .options(joinedload(Teacher.lessons))
             )
    result = await session.execute(query)
    teacher = result.scalars().first()

    if teacher:
        logger.info('Данные учителя получены успешно')
        return {
            'data': teacher,
            'detail': 'Данные учителя получены успешно',
        }
    else:
        logger.error('Не удалось получить данные учителя')
        raise HTTPException(status_code=404, detail="Не удалось получить данные учителя")
