from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models.user import Student
from api.configs.loggers import user_logger
from api.schemas.users.student import SStudent


@connection
async def get_student_for_id_util(student_id: int, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение студента')
    query = select(Student).where(Student.id == student_id).options(joinedload(Student.lessons))
    result = await session.execute(query)
    student = result.scalars().first()
    student_data = SStudent.from_orm(student)
    return {
        "data": student_data
    }
