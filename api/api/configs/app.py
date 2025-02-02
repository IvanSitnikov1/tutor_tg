from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings

from api.configs.loggers import system_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    system_logger.info('Сервер запущен.')
    yield
    system_logger.info('Сервер выключен.')


app = FastAPI(lifespan=lifespan)


class Settings(BaseSettings):
    DATABASE_URL: str
    class Config:
        env_file = ".env"


settings = Settings()
