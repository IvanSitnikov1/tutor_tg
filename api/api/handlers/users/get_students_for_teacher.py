from api.routers.user_router import user_router
from api.utils.users.get_students_for_teacher_util import get_students_for_teacher_util


@user_router.get(
    '/get_students_for_teacher',
    summary='Получение списка учеников запрашиваемого учителя',
    description='Эндпоинт возвращает список учеников запрашиваемого учителя',
)
async def get_students_for_teacher(teacher_tg_id: int):
    return await get_students_for_teacher_util(teacher_tg_id)
