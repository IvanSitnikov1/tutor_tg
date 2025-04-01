from api.routers.lesson_router import lesson_router
from api.utils.lessons.get_lesson_for_id_util import get_lesson_for_id_util


@lesson_router.get(
    '/{lesson_id}',
    summary='Получение урока по id',
    description='''
    Эндпоинт выполняет запрос на получение информации о уроке по его id.
    
    Параметры пути:
        lesson_id(int): id урока
    ''',
    responses={
        200: {
            "description": "Данные урока получены успешно",
            "content": {"application/json": {"example": {
                "data": {
                    "name": "lesson1",
                    "is_done": False,
                    "author_id": 1111111111,
                    "id": 1,
                    "date": "2025-04-01",
                    "student_id": 2222222222,
                    "completed_homeworks": [],
                    "comments_to_completed_homeworks": [],
                    "homeworks": [],
                    "files": [],
                },
                "detail": "Данные урока получены успешно",
            }}},
        },
        404: {
            "description": "Не удалось получить данные урока",
            "content": {"application/json": {"example": {
                "detail": "Не удалось получить данные урока",
            }}},
        },
    },
)
async def get_lesson_for_id(lesson_id: int):
    return await get_lesson_for_id_util(lesson_id)
