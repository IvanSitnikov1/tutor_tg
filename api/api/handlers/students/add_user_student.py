from api.routers.student_router import student_router
from api.schemas.student import SStudentAdd
from api.utils.students.add_user_student_util import add_user_student_util


@student_router.post(
    '',
    status_code=201,
    summary='Добавление пользователя студента',
    description='''
    Эндпоинт выполняет добавление пользователя студента.

    Тело запроса:
        Обязательные:
            user_name(str): имя студента
            id(int): telegram id пользователя
            teacher_id(int): telegram id учителя (код, полученный от учителя)
    ''',
)
async def add_user_student(user_data: SStudentAdd):
    return await add_user_student_util(user_data)
