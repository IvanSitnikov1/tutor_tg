from api.routers.user_router import user_router
from api.schemas.user import SAddPersonalFile
from api.utils.users.add_personal_file_util import add_personal_file_util


@user_router.post(
    '/add_personal_file',
)
async def add_personal_file(file_data: SAddPersonalFile):
    return await add_personal_file_util(file_data)
