from api.routers.lesson_router import lesson_router
from api.schemas.lesson import SDeleteFiles
from api.utils.lessons.delete_list_homeworks_util import delete_list_homeworks_util


@lesson_router.delete(
    '/homeworks',
    status_code=204,
    summary='Удаление нескольких домашних заданий',
    description='''
    Эндпоинт выполняет удаление нескольких домашних заданий, которые переданы в списке.
    
    Тело запроса:
        Обязательные:
            files_ids(list[int]): список id удаляемых домашних заданий
    ''',
    responses={
        204: {
            "description": "Домашние задания успешно удалены",
            "content": {"application/json": {"example": {
                "detail": "Домашние задания успешно удалены",
            }}},
        },
        400: {
            "description": "Не удалось удалить домашние задания",
            "content": {"application/json": {"example": {
                "detail": "Не удалось удалить домашние задания",
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
async def delete_list_homeworks(homeworks_data: SDeleteFiles):
    return await delete_list_homeworks_util(homeworks_data)
