from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.user import User
from api.configs.loggers import user_logger


@connection
async def get_users_util(session: AsyncSession):
    user_logger.info('Отправлен запрос на получение всех пользователей')
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    user_logger.info('Пользователи получены успешно')
    return {"data": users}
