from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.configs.database import connection
from api.models import Student, User
from api.schemas.student import SStudentAdd
from api.configs.loggers import logger


@connection
async def add_user_student_util(
        user_data: SStudentAdd,
        session: AsyncSession,
):
    logger.info(f'Получен запрос на создание пользователя студента - {user_data.username}')
    query = select(User).where(User.username == user_data.username)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        logger.error('Пользователь с таким именем уже существует')
        raise HTTPException(status_code=400, detail='Пользователь с таким именем уже существует')

    user = Student(type='student', **user_data.model_dump())
    session.add(user)
    try:
        await session.flush()
        await session.commit()
        await session.refresh(user)

        logger.info('Пользователь успешно добавлен')
        return {"data": user, "detail": "Пользователь успешно добавлен"}
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при добавлении пользователя: {e}')
        raise HTTPException(status_code=500, detail="Ошибка при добавлении пользователя!")
