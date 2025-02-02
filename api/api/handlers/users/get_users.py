from api.routers.user_router import user_router
from api.utils.users.get_users_util import get_users_util


@user_router.get(
    '/get_users',
    summary='Получение списка пользователей',
    description='Эндпоинт возвращает список пользователей',
)
async def get_users():
    return await get_users_util()
