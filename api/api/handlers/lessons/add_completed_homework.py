from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_completed_homework_util import add_completed_homework_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/completed_homeworks',
    status_code=201,
    summary=' Добавление выполненного домашнего задания',
    description='''
    Эндпоинт выполняет добавление выполненного домашнего задания.
    
    Тело запроса:
        Обязательные:
            lesson_id(int): id урока
            file_path(str): путь к файлу на диске в формате `completed_homeworks/file_name`
    '''
)
async def add_completed_homework(file: SFileAdd):
    return await add_completed_homework_util(file)
