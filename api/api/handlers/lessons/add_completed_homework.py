from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_completed_homework_util import add_completed_homework_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/completed_homeworks',
)
async def add_completed_homework(file: SFileAdd):
    return await add_completed_homework_util(file)
