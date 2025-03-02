from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.configs.database import connection
from api.models import Student, User
from api.schemas.student import SStudentAdd
from api.configs.loggers import user_logger


@connection
async def add_user_student_util(
        user_data: SStudentAdd,
        session: AsyncSession,
):
    user_logger.info(f'Получен запрос на создание студента с username - {user_data.username}')
    query = select(User).where(User.username == user_data.username)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='Пользователь с таким именем уже существует!')
    user = Student(type='student', **user_data.model_dump())
    session.add(user)
    try:
        await session.flush()
        await session.commit()
        await session.refresh(user)
        user_logger.info(f'Ученик с username - {user_data.username} успешно создан')
        return {"data": user, "detail": "Пользователь успешно добавлен"}
    except SQLAlchemyError:
        user_logger.error(f'Ошибка при добавлении пользователя в базу данных')
        raise HTTPException(status_code=400, detail="Ошибка при добавлении пользователя!")
