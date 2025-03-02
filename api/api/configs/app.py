from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings
from fastapi.staticfiles import StaticFiles

from api.configs.loggers import system_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    system_logger.info('Сервер запущен.')
    yield
    system_logger.info('Сервер выключен.')


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="../static"), name="static")


class Settings(BaseSettings):
    DATABASE_URL: str
    STATIC_PATH: str
    class Config:
        env_file = ".env"


settings = Settings()
