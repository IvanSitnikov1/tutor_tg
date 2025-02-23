from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import PersonalFile
from api.schemas.user import SAddPersonalFile
from api.configs.loggers import user_logger


@connection
async def add_personal_file_util(
        file_data: SAddPersonalFile,
        session: AsyncSession,
):
    file = PersonalFile(**file_data.model_dump())

    session.add(file)
    await session.commit()

    return {
        'data': file.file_path
    }
