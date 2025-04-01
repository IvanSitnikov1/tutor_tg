from api.routers.teacher_router import teacher_router
from api.utils.teachers.get_teacher_by_id_util import get_teacher_by_id_util


@teacher_router.get(
    '/{teacher_id}',
    summary='Получение учителя по id',
    description='''
    Эндпоинт выполняет запрос на получение информации о учителе по его id.
    
    Параметры пути:
        teacher_id(int): id учителя
    ''',
    responses={
        200: {
            "description": "Данные учителя получены успешно",
            "content": {"application/json": {"example": {
                "data": {
                    "username": "test_user",
                    "id": 1111111111,
                    "type": "teacher",
                    "personal_files": [],
                    "lessons": [],
                    "students": [],
                },
                "detail": "Данные учителя получены успешно",
            }}},
        },
        404: {
            "description": "Не удалось получить данные учителя",
            "content": {"application/json": {"example": {
                "detail": "Не удалось получить данные учителя",
            }}},
        },
    },
)
async def get_teacher_by_id(teacher_id: int):
    return await get_teacher_by_id_util(teacher_id)
