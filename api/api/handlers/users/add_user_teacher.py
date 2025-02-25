from api.routers.user_router import user_router
from api.schemas.user import STeacherAdd
from api.utils.users.add_user_teacher_util import add_user_teacher_util


@user_router.post(
    '/teacher',
    status_code=201,
    summary='Добавление пользователя учителя',
    description='Эндпоинт принимает данные нового пользователя учителя и создает его. '
                'Возвращает данные нового пользователя.',
)
async def add_user_teacher(user: STeacherAdd):
    return await add_user_teacher_util(user)
