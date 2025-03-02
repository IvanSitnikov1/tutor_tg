from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_lesson_util import add_lesson_util

from api.schemas.lesson import SLessonAdd


@lesson_router.post(
    '',
)
async def add_lesson(lesson: SLessonAdd):
    return await add_lesson_util(lesson)
