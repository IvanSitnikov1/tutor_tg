from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_lesson_util import add_lesson_util

from api.schemas.lesson import SLessonAdd


@lesson_router.post(
    '',
    status_code=201,
    summary='Добавление урока',
    description='''
    Эндпоинт выполняет добавление урока.
    
    Тело запроса:
        Обязательные:
            name(str): название урока
            student_id(int): id студента
            author_id(int): id учителя автора
    ''',
)
async def add_lesson(lesson: SLessonAdd):
    return await add_lesson_util(lesson)
