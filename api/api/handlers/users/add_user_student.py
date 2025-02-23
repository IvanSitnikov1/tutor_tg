from api.routers.user_router import user_router
from api.schemas.user import UserStudentAdd
from api.utils.users.add_user_student_util import add_user_student_util


@user_router.post(
    '/add_user_student',
    status_code=201,
    summary='Добавление пользователя студента',
    description='Эндпоинт принимает данные нового пользователя студента и создает его. '
                'Возвращает данные нового пользователя.',
)
async def add_user_student(user: UserStudentAdd):
    return await add_user_student_util(user)
