from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_file_in_lesson_util import add_file_in_lesson_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/add_file_in_lesson',
    summary='Получение данных ученика по id',
    description='Эндпоинт возвращает данные ученика',
)
async def add_file_in_lesson(file: SFileAdd):
    return await add_file_in_lesson_util(file)
