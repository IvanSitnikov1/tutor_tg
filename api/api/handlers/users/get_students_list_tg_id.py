from api.routers.user_router import user_router
from api.utils.users.get_students_list_tg_id_util import get_students_list_tg_id_util


@user_router.get(
    '/students/list_tg_id',
)
async def get_students_list_tg_id():
    return await get_students_list_tg_id_util()
