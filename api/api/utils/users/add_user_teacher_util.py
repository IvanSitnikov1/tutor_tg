from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.user import Teacher
from api.schemas.user import STeacherAdd
from api.configs.loggers import user_logger


@connection
async def add_user_teacher_util(
        user: STeacherAdd,
        session: AsyncSession,
):
    user_logger.info(f'Получен запрос на создание учителя с username - {user.username}')
    user_data = user.model_dump()
    user = Teacher(type='teacher', **user_data)
    session.add(user)
    try:
        await session.flush()
        await session.commit()
        await session.refresh(user)
        user_logger.info(f'Учитель с username - {user.username} успешно создан')
        return {"data": user, "detail": "Пользователь успешно добавлен"}
    except IntegrityError as e:
        if 'unique' in str(e.orig).lower():
            user_logger.error('Данный пользователь уже существует!')
            raise HTTPException(status_code=400, detail='Данный пользователь уже существует!')
        user_logger.error(f'Ошибка при добавлении пользователя!')
        raise HTTPException(status_code=400, detail="Ошибка при добавлении пользователя!")
