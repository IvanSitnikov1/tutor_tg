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
    responses={
        201: {
            "description": "Урок добавлен успешно",
            "content": {"application/json": {"example": {
                "data": {
                    "name": "test_lesson",
                    "is_done": False,
                    "author_id": 1111111111,
                    "id": 1,
                    "date": "2025-04-01",
                    "student_id": 2222222222,
                },
                "detail": "Урок добавлен успешно",
            }}},
        },
        500: {
            "description": "Ошибка при добавлении урока",
            "content": {"application/json": {"example": {
                "detail": "Ошибка при добавлении урока",
            }}},
        },
    },
)
async def add_lesson(lesson: SLessonAdd):
    return await add_lesson_util(lesson)
