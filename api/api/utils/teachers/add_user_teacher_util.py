from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from  sqlalchemy import select

from api.configs.database import connection
from api.models import Teacher, User
from api.schemas.teacher import STeacherAdd
from api.configs.loggers import user_logger


@connection
async def add_user_teacher_util(
        user_data: STeacherAdd,
        session: AsyncSession,
):
    user_logger.info(f'Получен запрос на создание учителя с username - {user_data.username}')
    query = select(User).where(User.username == user_data.username)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='Пользователь с таким именем уже существует!')
    user = Teacher(type='teacher', **user_data.model_dump())
    session.add(user)
    try:
        await session.flush()
        await session.commit()
        await session.refresh(user)
        user_logger.info(f'Учитель с username - {user_data.username} успешно создан')
        return {"data": user, "detail": "Пользователь успешно добавлен"}
    except SQLAlchemyError:
        user_logger.error(f'Ошибка при добавлении пользователя в базу данных')
        raise HTTPException(status_code=400, detail="Ошибка при добавлении пользователя!")
