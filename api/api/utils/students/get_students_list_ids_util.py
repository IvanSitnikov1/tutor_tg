from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from api.configs.database import connection
from api.models import Student
from api.configs.loggers import logger


@connection
async def get_students_list_ids_util(session: AsyncSession):
    logger.info('Получен запрос на получение списка id всех студентов')
    query = select(Student.id)
    result = await session.execute(query)
    if result:
        logger.info('Список id студентов получен успешно')
        return {
            "data": result.scalars().all(),
            "detail": "Список id студентов получен успешно",
        }
    else:
        logger.error('Не удалось получить список id студентов')
        raise HTTPException(status_code=404, detail="Не удалось получить список id студентов")
