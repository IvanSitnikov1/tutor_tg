from api.routers.lesson_router import lesson_router
from api.utils.lessons.delete_lesson_util import delete_lesson_util


@lesson_router.delete(
    '/{lesson_id}',
    status_code=204,
    summary='Удаление урока',
    description='''
    Эндпоинт выполняет удаление урока и всех файлов урока.
    
    Параметры пути:
        lesson_id(int): id урока
    ''',
)
async def delete_lesson(lesson_id: int):
    return await delete_lesson_util(lesson_id)
