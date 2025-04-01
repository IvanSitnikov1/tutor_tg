from api.routers.lesson_router import lesson_router
from api.utils.lessons.add_file_util import add_file_util

from api.schemas.lesson import SFileAdd


@lesson_router.post(
    '/files',
    status_code=201,
    summary='Добавление материала в урок',
    description='''
    Эндпоинт выполняет добавление файла материала в урок.
    
    Тело запроса:
        Обязательные:
            lesson_id(int): id урока
            file_path(str): путь к файлу на диске в формате `files/file_name`
    ''',
    responses={
        201: {
            "description": "Файл добавлен успешно",
            "content": {"application/json": {"example": {
                "detail": "Файл добавлен успешно",
            }}},
        },
        500: {
            "description": "Ошибка при добавлении файла",
            "content": {"application/json": {"example": {
                "detail": "Ошибка при добавлении файла",
            }}},
        },
    },
)
async def add_file(file: SFileAdd):
    return await add_file_util(file)
