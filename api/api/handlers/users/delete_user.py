from api.routers.user_router import user_router
from api.utils.users.delete_user_util import delete_user_util


@user_router.delete(
    '',
    status_code=204,
    summary='Удаление пользователя',
    description='Эндпоинт удаляет пользователя по переданному tg_id.'
)
async def delete_user(user_tg_id: int):
    return await delete_user_util(user_tg_id)
