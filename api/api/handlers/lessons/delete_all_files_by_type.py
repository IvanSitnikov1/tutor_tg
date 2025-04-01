from api.routers.lesson_router import lesson_router
from api.utils.lessons.delete_all_files_by_type_util import delete_all_files_by_type_util


@lesson_router.delete(
    '/{lesson_id}/{file_type}',
    status_code=204,
    summary='Удаление всех файлов урока определенного типа',
    description='''
    Эндпоинт выполняет удаление всех файлов указанного типа из урока.
    
    Параметры пути:
        lesson_id(int): id урока
        file_type(str): тип удаляемых файлов
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
async def delete_all_files_by_type(lesson_id: int, file_type: str):
    return await delete_all_files_by_type_util(lesson_id, file_type)
