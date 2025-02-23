from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.user import Student
from api.schemas.user import UserStudentAdd
from api.configs.loggers import user_logger


@connection
async def add_user_student_util(
        user: UserStudentAdd,
        session: AsyncSession,
):
    user_logger.info(f'Получен запрос на создание студента с username - {user.username}')
    user_data = user.model_dump()
    user = Student(type='student', **user_data)
    session.add(user)
    try:
        await session.flush()
        await session.commit()
        await session.refresh(user)
        user_logger.info(f'Студент с username - {user.username} успешно создан')
        return {"data": user, "detail": "Пользователь успешно добавлен"}
    except IntegrityError as e:
        if 'unique' in str(e.orig).lower():
            user_logger.error('Данный пользователь уже существует!')
            raise HTTPException(status_code=400, detail='Данный пользователь уже существует!')
        elif 'foreign key constraint' in str(e.orig).lower():
            user_logger.error('Указанного учителя не существует!')
            raise HTTPException(status_code=400, detail="Указанного учителя не существует!")
        else:
            user_logger.error(f'Ошибка при добавлении пользователя!')
            raise HTTPException(status_code=400, detail="Ошибка при добавлении пользователя!")
