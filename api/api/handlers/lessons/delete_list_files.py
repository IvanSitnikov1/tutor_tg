from api.routers.lesson_router import lesson_router
from api.schemas.lesson import SDeleteFiles
from api.utils.lessons.delete_list_files_util import delete_list_files_util


@lesson_router.delete(
    '/files',
    status_code=204,
    summary='Удаление нескольких материалов урока',
    description='''
    Эндпоинт выполняет удаление нескольких материалов урока, которые переданы в списке.
    
    Тело запроса:
        Обязательные:
            files_ids(list[int]): список id удаляемых материалов
    ''',
    responses={
        204: {
            "description": "Файлы лекции успешно удалены",
            "content": {"application/json": {"example": {
                "detail": "Файлы лекции успешно удалены",
            }}},
        },
        400: {
            "description": "Не удалось удалить файлы лекции",
            "content": {"application/json": {"example": {
                "detail": "Не удалось удалить файлы лекции",
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
async def delete_list_files(files_data: SDeleteFiles):
    return await delete_list_files_util(files_data)
