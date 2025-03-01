from api.routers.user_router import user_router
from api.utils.users.get_student_for_tg_id_util import get_student_for_tg_id_util


@user_router.get(
    '/students/student/tg_id/{student_tg_id}',
    summary='Получение списка учеников запрашиваемого учителя',
    description='Эндпоинт возвращает список учеников запрашиваемого учителя',
)
async def get_student_for_tg_id(student_tg_id: int):
    return await get_student_for_tg_id_util(student_tg_id)
