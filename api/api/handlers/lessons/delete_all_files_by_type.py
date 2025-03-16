from api.routers.lesson_router import lesson_router
from api.utils.lessons.delete_all_files_by_type_util import delete_all_files_by_type_util


@lesson_router.delete(
    '/{lesson_id}/{file_type}',
)
async def delete_all_files_by_type(lesson_id: int, file_type: str):
    return await delete_all_files_by_type_util(lesson_id, file_type)
