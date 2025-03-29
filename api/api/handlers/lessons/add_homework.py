from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_homework_util import add_homework_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/homeworks',
    status_code=201,
    summary='Добавление домашнего задания',
    description='''
    Эндпоинт выполняет добавление файла домашнего задания.
    
    Тело запроса:
        Обязательные:
            lesson_id(int): id урока
            file_path(str): путь к файлу на диске в формате `homeworks/file_name`
    ''',
)
async def add_homework(file: SFileAdd):
    return await add_homework_util(file)
