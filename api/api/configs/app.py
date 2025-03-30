from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.configs.loggers import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Сервер запущен.')
    yield
    logger.info('Сервер выключен.')


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="../static"), name="static")


class Settings(BaseSettings):
    DATABASE_URL: str
    STATIC_PATH: str
    class Config:
        env_file = ".env"


settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://217.114.10.190"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
