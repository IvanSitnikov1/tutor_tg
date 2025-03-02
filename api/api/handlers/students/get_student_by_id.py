from api.routers.student_router import student_router
from api.utils.students.get_student_by_id_util import get_student_by_id_util


@student_router.get(
    '/{student_id}',
    summary='Получение данных ученика по id',
    description='Эндпоинт возвращает данные ученика',
)
async def get_student_by_id(student_id: int):
    return await get_student_by_id_util(student_id)
