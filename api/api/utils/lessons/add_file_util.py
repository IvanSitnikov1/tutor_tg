from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models.file import File
from api.schemas.lesson import SFileAdd


@connection
async def add_file_util(file: SFileAdd, session: AsyncSession):
    new_file = File(**file.model_dump())
    session.add(new_file)

    try:
        await session.commit()
        return {
            "detail": "Файл добавлен успешно"
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Ошибка при добавлении файла")
