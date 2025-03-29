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
)
async def delete_all_files_by_type(lesson_id: int, file_type: str):
    return await delete_all_files_by_type_util(lesson_id, file_type)
