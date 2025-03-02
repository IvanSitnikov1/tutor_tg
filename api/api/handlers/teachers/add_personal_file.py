from api.routers.teacher_router import teacher_router
from api.schemas.teacher import SPersonalFileAdd
from api.utils.teachers.add_personal_file_util import add_personal_file_util


@teacher_router.post(
    '/personal_files',
)
async def add_personal_file(file_data: SPersonalFileAdd):
    return await add_personal_file_util(file_data)
