from api.routers.teacher_router import teacher_router
from api.schemas.lesson import SDeleteFiles
from api.utils.teachers.delete_list_personal_files_util import delete_list_personal_files_util


@teacher_router.delete(
    '/personal_files',
    status_code=204,
    summary='Удаление нескольких личных файлов',
    description='''
    Эндпоинт выполняет удаление нескольких личных файлов учителя, которые переданы в списке.
    
    Тело запроса:
        Обязательные:
            files_ids(list[int]): список id удаляемых личных файлов
    ''',
)
async def delete_list_personal_files(personal_files_data: SDeleteFiles):
    return await delete_list_personal_files_util(personal_files_data)
