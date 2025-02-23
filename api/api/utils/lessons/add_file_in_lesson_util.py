from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.file import File
from api.configs.loggers import user_logger
from api.schemas.lesson import SFileAdd


@connection
async def add_file_in_lesson_util(file: SFileAdd, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение студента')
    new_file = File(**file.model_dump())
    session.add(new_file)
    await session.commit()
    return {
        "data": "file add successfully"
    }
