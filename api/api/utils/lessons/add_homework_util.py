from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.file import Homework
from api.configs.loggers import user_logger
from api.schemas.lesson import SFileAdd


@connection
async def add_homework_util(file: SFileAdd, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение студента')
    new_homework = Homework(**file.model_dump())
    session.add(new_homework)
    await session.commit()
    return {
        "data": "homework add successfully"
    }
