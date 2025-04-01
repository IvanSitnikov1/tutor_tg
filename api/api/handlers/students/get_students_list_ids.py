from api.routers.student_router import student_router
from api.utils.students.get_students_list_ids_util import get_students_list_ids_util


@student_router.get(
    '',
    summary='Получение списка id студентов',
    description='''
    Эндпоинт получает список id всех студентов.
    ''',
    responses={
        200: {
            "description": "Список id студентов получен успешно",
            "content": {"application/json": {"example": {
                "data": [1111111111, 2222222222],
                "detail": "Список id студентов получен успешно",
            }}},
        },
        404: {
            "description": "Не удалось получить список id студентов",
            "content": {"application/json": {"example": {
                "detail": "Не удалось получить список id студентов",
            }}},
        },
    },
)
async def get_students_list_ids():
    return await get_students_list_ids_util()
