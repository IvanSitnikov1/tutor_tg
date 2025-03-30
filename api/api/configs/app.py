from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from api.configs.loggers import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Сервер запущен.')
    yield
    logger.info('Сервер выключен.')


app = FastAPI(lifespan=lifespan)
# app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="../static"), name="static")


class Settings(BaseSettings):
    DATABASE_URL: str
    STATIC_PATH: str
    class Config:
        env_file = ".env"


settings = Settings()


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        swagger_ui_parameters={"supportedSubmitMethods": []}
    )
