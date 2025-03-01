from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.configs.database import connection
from api.models import Lesson, Student
from api.configs.loggers import user_logger
from api.schemas.user import SStudent


@connection
async def get_student_for_id_util(student_id: int, session: AsyncSession):
    user_logger.info('Отправлен запрос на получение студента')
    query = (
        select(Student)
        .where(Student.id == student_id)
        .options(
            joinedload(Student.lessons).joinedload(Lesson.files),
            joinedload(Student.lessons).joinedload(Lesson.homeworks),
            joinedload(Student.lessons).joinedload(Lesson.completed_homeworks),
            joinedload(Student.lessons).joinedload(Lesson.comments_by_completed_homeworks),
        )
    )

    result = await session.execute(query)
    student = result.scalars().first()
    if student:
        student_data = SStudent.model_validate(student)
    else:
        student_data = {
            "detail": 'Нет такого студента'
        }
    return {
        "data": student_data
    }
