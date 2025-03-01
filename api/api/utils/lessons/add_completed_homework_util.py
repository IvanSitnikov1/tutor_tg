from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import CompletedHomeworks
from api.schemas.lesson import SFileAdd


@connection
async def add_completed_homework_util(file: SFileAdd, session: AsyncSession):
    new_file = CompletedHomeworks(**file.model_dump())
    session.add(new_file)
    await session.commit()
    return {
        "data": "file add successfully"
    }
