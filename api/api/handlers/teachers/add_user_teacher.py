from api.routers.teacher_router import teacher_router
from api.schemas.teacher import STeacherAdd
from api.utils.teachers.add_user_teacher_util import add_user_teacher_util


@teacher_router.post(
    '',
    status_code=201,
    summary='Добавление пользователя учителя',
    description='''
    Эндпоинт выполняет добавление пользователя учителя.

    Тело запроса:
        Обязательные:
            user_name(str): имя учителя
            id(int): telegram id пользователя
    ''',
)
async def add_user_teacher(user_data: STeacherAdd):
    return await add_user_teacher_util(user_data)
