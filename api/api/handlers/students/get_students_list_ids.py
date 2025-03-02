from api.routers.student_router import student_router
from api.utils.students.get_students_list_ids_util import get_students_list_ids_util


@student_router.get(
    '',
)
async def get_students_list_ids():
    return await get_students_list_ids_util()
