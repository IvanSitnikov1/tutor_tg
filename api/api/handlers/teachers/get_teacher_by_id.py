from api.routers.teacher_router import teacher_router
from api.utils.teachers.get_teacher_by_id_util import get_teacher_by_id_util


@teacher_router.get(
    '/{teacher_id}',
    summary='Получение учителя по id',
    description='''
    Эндпоинт выполняет запрос на получение информации о учителе по его id.
    
    Параметры пути:
        teacher_id(int): id учителя
    ''',
)
async def get_teacher_by_id(teacher_id: int):
    return await get_teacher_by_id_util(teacher_id)
