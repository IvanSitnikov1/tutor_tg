from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_file_util import add_file_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/files',
    summary='Получение данных ученика по id',
    description='Эндпоинт возвращает данные ученика',
)
async def add_file(file: SFileAdd):
    return await add_file_util(file)
