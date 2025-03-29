import os

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from api.configs.app import settings
from api.configs.database import connection
from api.models import Student, Lesson, User
from api.configs.loggers import logger


@connection
async def delete_user_student_util(student_id: int, session: AsyncSession):
    logger.info('Получен запрос на удаление пользователя студента')
    query = select(Student).where(Student.id == student_id).options(
        selectinload(Student.lessons).options(
            selectinload(Lesson.files),
            selectinload(Lesson.homeworks),
            selectinload(Lesson.completed_homeworks),
            selectinload(Lesson.comments_to_completed_homeworks),
        ),
    )

    result = await session.execute(query)
    student = result.scalar_one_or_none()
    if not student:
        logger.error('Студент не найден')
        raise HTTPException(status_code=404, detail='Студент не найден')

    logger.info('Удаление пользователя ученика из базы данных...')
    stmt = delete(User).where(User.id == student_id)
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount:
        logger.info('Удаление файлов с сервера...')
        for lesson in student.lessons:
            for file_list in [
                lesson.files,
                lesson.homeworks,
                lesson.completed_homeworks,
                lesson.comments_to_completed_homeworks
            ]:
                for file in file_list:
                    file_path = settings.STATIC_PATH + file.file_path
                    if os.path.exists(file_path):
                        os.remove(file_path)

        logger.info('Ученик удален успешно')
        return {
            'detail': 'Ученик удален успешно',
        }
    else:
        logger.error('Не удалось удалить пользователя студента')
        raise HTTPException(status_code=400, detail='Не удалось удалить пользователя студента')
