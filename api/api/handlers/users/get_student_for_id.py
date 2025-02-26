from api.routers.user_router import user_router
from api.utils.users.get_student_for_id_util import get_student_for_id_util


@user_router.get(
    '/students/{student_id}',
    summary='Получение данных ученика по id',
    description='Эндпоинт возвращает данные ученика',
)
async def get_student_for_id(student_id: int):
    return await get_student_for_id_util(student_id)
