from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models.user import Teacher
from api.configs.loggers import user_logger


@connection
async def get_students_for_teacher_util(teacher_tg_id, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение списка студентов учителя')
    query = select(Teacher).where(Teacher.tg_id == teacher_tg_id).options(joinedload(Teacher.students))
    result = await session.execute(query)
    teacher = result.scalars().first()
    user_logger.info('Список студентов получен успешно')
    return {"data": teacher.students}
