from api.routers.lesson_router import lesson_router
from api.utils.lessons.change_lesson_is_done_util import change_lesson_is_done_util


@lesson_router.get(
    '/{lesson_id}/change_is_done',
    summary='Получение данных ученика по id',
    description='Эндпоинт возвращает данные ученика',
)
async def change_lesson_is_done(lesson_id: int):
    return await change_lesson_is_done_util(lesson_id)
