from api.routers.lesson_router import lesson_router
from api.utils.lessons.change_lesson_is_done_util import change_lesson_is_done_util


@lesson_router.get(
    '/{lesson_id}/change_is_done',
    summary='Изменение состояния урока (выполнен/не выполнен)',
    description='''
    Эндпоинт выполняет изменение состояния урока (выполнен/не выполнен) на противоположное.
    
    Параметры пути:
        lesson_id(int): id урока
    ''',
    responses={
        200: {
            "description": "Состояние урока изменено успешно",
            "content": {"application/json": {"example": {
                "data": True,
                "detail": "Состояние урока изменено успешно",
            }}},
        },
        404: {
            "description": "Запрашиваемого урока не существует",
            "content": {"application/json": {"example": {
                "detail": "Запрашиваемого урока не существует",
            }}},
        },
        500: {
            "description": "Ошибка при изменении состояния урока",
            "content": {"application/json": {"example": {
                "detail": "Ошибка при изменении состояния урока",
            }}},
        },
    },
)
async def change_lesson_is_done(lesson_id: int):
    return await change_lesson_is_done_util(lesson_id)
