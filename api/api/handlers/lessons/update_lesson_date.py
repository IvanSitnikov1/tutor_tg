from api.routers.lesson_router import lesson_router
from api.utils.lessons.update_lesson_date_util import update_lesson_date_util


@lesson_router.put(
    '/{lesson_id}',
    summary='Изменение даты урока',
    description='''
    Эндпоинт выполняет изменение даты урока.
    
    Параметры пути:
        lesson_id(int): id урока
    ''',
)
async def update_lesson_date(lesson_id: int, new_date: str):
    return await update_lesson_date_util(lesson_id, new_date)
