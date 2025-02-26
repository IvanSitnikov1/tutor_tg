from api.routers.user_router import user_router
from api.schemas.lesson import SDeleteFiles
from api.utils.users.delete_list_personal_files_util import delete_list_personal_files_util


@user_router.delete(
    '/files',
)
async def delete_list_personal_files(personal_files_data: SDeleteFiles):
    return await delete_list_personal_files_util(personal_files_data)
