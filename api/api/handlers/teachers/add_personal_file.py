from api.routers.teacher_router import teacher_router
from api.schemas.teacher import SPersonalFileAdd
from api.utils.teachers.add_personal_file_util import add_personal_file_util


@teacher_router.post(
    '/personal_files',
    status_code=201,
    summary='Добавление личного файла',
    description='''
    Эндпоинт выполняет добавление личного файла для учителя.
    
    Тело запроса:
        Обязательные:
            author_id(int): id учителя
            file_path(str): путь к файлу на диске в формате `personal_files/file_name`
    ''',
    responses={
        201: {
            "description": "Файл успешно добавлен",
            "content": {"application/json": {"example": {
                "data": {
                    "id": 1,
                    "author_id": 1111111111,
                    "file_path": "/personal_files/file_name.pdf",
                },
                "detail": "Файл успешно добавлен",
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
async def add_personal_file(file_data: SPersonalFileAdd):
    return await add_personal_file_util(file_data)
