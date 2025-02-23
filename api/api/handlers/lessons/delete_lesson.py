from api.routers.lesson_router import lesson_router
from api.utils.lessons.delete_lesson_util import delete_lesson_util


@lesson_router.delete(
    '/delete_lesson',
    summary='Получение данных ученика по id',
    description='Эндпоинт возвращает данные ученика',
)
async def delete_lesson(lesson_id: int):
    return await delete_lesson_util(lesson_id)
