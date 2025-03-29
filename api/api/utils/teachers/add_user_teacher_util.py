from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from  sqlalchemy import select

from api.configs.database import connection
from api.models import Teacher, User
from api.schemas.teacher import STeacherAdd
from api.configs.loggers import logger


@connection
async def add_user_teacher_util(
        user_data: STeacherAdd,
        session: AsyncSession,
):
    logger.info(f'Получен запрос на создание пользователя учителя - {user_data.username}')
    query = select(User).where(User.username == user_data.username)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        logger.error('Пользователь с таким именем уже существует')
        raise HTTPException(status_code=400, detail='Пользователь с таким именем уже существует')

    user = Teacher(type='teacher', **user_data.model_dump())
    session.add(user)
    try:
        await session.flush()
        await session.commit()
        await session.refresh(user)

        logger.info('Пользователь успешно добавлен')
        return {"data": user, "detail": "Пользователь успешно добавлен"}
    except SQLAlchemyError as e:
        logger.error(f'Ошибка при добавлении пользователя: {e}')
        raise HTTPException(status_code=500, detail="Ошибка при добавлении пользователя")
