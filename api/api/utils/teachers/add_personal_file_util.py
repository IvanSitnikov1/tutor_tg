from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession

from api.configs.database import connection
from api.models import PersonalFile
from api.schemas.teacher import SPersonalFileAdd


@connection
async def add_personal_file_util(
        file_data: SPersonalFileAdd,
        session: AsyncSession,
):
    file = PersonalFile(**file_data.model_dump())
    session.add(file)
    try:
        await session.flush()
        await session.commit()
        await session.refresh(file)

        return {
            'data': file,
            'detail': 'Файл успешно добавлен',
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Ошибка при добавлении файла")
