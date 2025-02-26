from api.routers.user_router import user_router
from api.utils.users.get_teacher_for_tg_id_util import get_teacher_for_tg_id_util


@user_router.get(
    '/teachers/{teacher_tg_id}',
    summary='Получение списка учеников запрашиваемого учителя',
    description='Эндпоинт возвращает список учеников запрашиваемого учителя',
)
async def get_teacher_for_tg_id(teacher_tg_id: int):
    return await get_teacher_for_tg_id_util(teacher_tg_id)
