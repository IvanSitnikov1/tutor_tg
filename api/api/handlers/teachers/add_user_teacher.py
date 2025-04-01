from api.routers.teacher_router import teacher_router
from api.schemas.teacher import STeacherAdd
from api.utils.teachers.add_user_teacher_util import add_user_teacher_util


@teacher_router.post(
    '',
    status_code=201,
    summary='Добавление пользователя учителя',
    description='''
    Эндпоинт выполняет добавление пользователя учителя.

    Тело запроса:
        Обязательные:
            user_name(str): имя учителя
            id(int): telegram id пользователя
    ''',
    responses={
        201: {
            "description": "Состояние урока изменено успешно",
            "content": {"application/json": {"example": {
                "data": {
                    "username": "test_user",
                    "teacher_id": 1111111111,
                    "type": "student",
                    "id": 2222222222
                },
                "detail": "Пользователь успешно добавлен",
            }}},
        },
        400: {
            "description": "Пользователь с таким именем уже существует",
            "content": {"application/json": {"example": {
                "detail": "Пользователь с таким именем уже существует",
            }}},
        },
        500: {
            "description": "Ошибка при добавлении пользователя",
            "content": {"application/json": {"example": {
                "detail": "Ошибка при добавлении пользователя",
            }}},
        },
    },
)
async def add_user_teacher(user_data: STeacherAdd):
    return await add_user_teacher_util(user_data)
