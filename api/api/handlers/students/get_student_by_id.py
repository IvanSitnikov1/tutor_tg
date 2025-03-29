from api.routers.student_router import student_router
from api.utils.students.get_student_by_id_util import get_student_by_id_util


@student_router.get(
    '/{student_id}',
    summary='Получение студента по id',
    description='''
    Эндпоинт выполняет запрос на получение информации о студенте по его id.

    Параметры пути:
        student_id(int): id студента
    ''',
)
async def get_student_by_id(student_id: int):
    return await get_student_by_id_util(student_id)
