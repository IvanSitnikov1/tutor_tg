from api.routers.lesson_router import lesson_router
from api.utils.lessons.update_lesson_date_util import update_lesson_date_util


@lesson_router.put(
    '/{lesson_id}',
    summary='Изменение даты урока',
    description='''
    Эндпоинт выполняет изменение даты урока.
    
    Параметры пути:
        lesson_id(int): id урока
    Параметры запроса:
        new_date(str): новая дата урока в формате дд-мм-гггг
    ''',
    responses={
        200: {
            "description": "Дата лекции обновлена успешно",
            "content": {"application/json": {"example": {
                "data": "26-01-2024",
                "detail": "Дата лекции обновлена успешно",
            }}},
        },
        400: {
            "description": "Переданный формат даты не соответствует ожидаемому - %d-%m-%Y",
            "content": {"application/json": {"example": {
                "detail": "Переданный формат даты не соответствует ожидаемому - %d-%m-%Y",
            }}},
        },
        500: {
            "description": "Ошибка при обновлении даты лекции",
            "content": {"application/json": {"example": {
                "detail": "Ошибка при обновлении даты лекции",
            }}},
        },
    },
)
async def update_lesson_date(lesson_id: int, new_date: str):
    return await update_lesson_date_util(lesson_id, new_date)
