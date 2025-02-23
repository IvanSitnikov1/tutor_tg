from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_homework_util import add_homework_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/add_homework',
    summary='Получение данных ученика по id',
    description='Эндпоинт возвращает данные ученика',
)
async def add_homework(file: SFileAdd):
    return await add_homework_util(file)
