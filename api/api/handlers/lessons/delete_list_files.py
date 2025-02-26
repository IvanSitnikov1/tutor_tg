from api.routers.lesson_router import lesson_router
from api.schemas.lesson import SDeleteFiles
from api.utils.lessons.delete_list_files_util import delete_list_files_util


@lesson_router.delete(
    '/files',
)
async def delete_list_files(files_data: SDeleteFiles):
    return await delete_list_files_util(files_data)
