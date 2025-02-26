from api.routers.lesson_router import lesson_router
from api.schemas.lesson import SDeleteFiles
from api.utils.lessons.delete_list_homeworks_util import delete_list_homeworks_util


@lesson_router.delete(
    '/homeworks',
)
async def delete_list_homeworks(homeworks_data: SDeleteFiles):
    return await delete_list_homeworks_util(homeworks_data)
