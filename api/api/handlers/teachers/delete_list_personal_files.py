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
    responses={
        204: {
            "description": "Выбранные персональные файлы успешно удалены",
            "content": {"application/json": {"example": {
                "detail": "Выбранные персональные файлы успешно удалены",
            }}},
        },
        400: {
            "description": "Не удалось удалить выбранные персональные файлы",
            "content": {"application/json": {"example": {
                "detail": "Не удалось удалить выбранные персональные файлы",
            }}},
        },
        404: {
            "description": "Файлы не найдены",
            "content": {"application/json": {"example": {
                "detail": "Файлы не найдены",
            }}},
        },
    },
)
async def delete_list_personal_files(personal_files_data: SDeleteFiles):
    return await delete_list_personal_files_util(personal_files_data)
