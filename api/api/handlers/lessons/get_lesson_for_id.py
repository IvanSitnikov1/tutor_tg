from api.routers.lesson_router import lesson_router
from api.utils.lessons.get_lesson_for_id_util import get_lesson_for_id_util


@lesson_router.get(
    '/{lesson_id}',
    summary='Получение данных ученика по id',
    description='Эндпоинт возвращает данные ученика',
)
async def get_lesson_for_id(lesson_id: int):
    return await get_lesson_for_id_util(lesson_id)
