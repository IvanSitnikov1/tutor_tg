from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base

from api.configs.app import settings


Base = declarative_base(cls=AsyncAttrs)
engine = create_async_engine(settings.DATABASE_URL, echo=False)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def connection(method):
    """
    Функция-декоратор для безопасной работы с базой данных
    """
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откат транзакции при ошибке
                raise e
    return wrapper
