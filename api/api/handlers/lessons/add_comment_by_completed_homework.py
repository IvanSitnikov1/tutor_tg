from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_comment_by_completed_homework_util import add_comment_by_completed_homework_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/comments_by_completed_homeworks',
)
async def add_comments_by_completed_homework(file: SFileAdd):
    return await add_comment_by_completed_homework_util(file)
