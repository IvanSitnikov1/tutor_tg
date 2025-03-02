from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_homework_util import add_homework_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/homeworks',
)
async def add_homework(file: SFileAdd):
    return await add_homework_util(file)
