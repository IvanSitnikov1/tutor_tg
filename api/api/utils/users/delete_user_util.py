from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from api.configs.database import connection
from api.models.user import User
from api.configs.loggers import user_logger


@connection
async def delete_user_util(user_tg_id: int, session: AsyncSession):
    user_logger.info('Отправлен запрос на удаление пользователя')
    query = delete(User).where(User.tg_id == user_tg_id)
    result = await session.execute(query)

    if result.rowcount:
        await session.commit()
        user_logger.info(f"Пользователь  успешно удален")
    else:
        user_logger.error(f'Данного пользователя не существует!')
        raise HTTPException(status_code=400, detail=f"Данного пользователя не существует!")
