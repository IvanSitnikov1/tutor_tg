from logging.config import fileConfig
import asyncio

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from api.models import Base
from api.configs.app import settings


config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata


url = settings.DATABASE_URL

engine = create_async_engine(url, poolclass=pool.NullPool)



async def run_migrations():
    """Асинхронный запуск миграций."""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Запуск синхронных миграций."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

asyncio.run(run_migrations())
