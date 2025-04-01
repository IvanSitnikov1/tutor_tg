from api.routers.student_router import student_router
from api.utils.students.delete_user_student_util import delete_user_student_util


@student_router.delete(
    '/{student_id}',
    summary='Удаление пользователя студента',
    description='''
    Эндпоинт выполняет удаление пользователя студента со всеми его уроками и файлами.
    
    Параметры пути:
        student_id(int): id студента
    ''',
    responses={
        200: {
            "description": "Состояние урока изменено успешно",
            "content": {"application/json": {"example": {
                "detail": "Ученик удален успешно",
            }}},
        },
        400: {
            "description": "Не удалось удалить пользователя студента",
            "content": {"application/json": {"example": {
                "detail": "Не удалось удалить пользователя студента",
            }}},
        },
        404: {
            "description": "Студент не найден",
            "content": {"application/json": {"example": {
                "detail": "Студент не найден",
            }}},
        },
    },
)
async def delete_user_student(student_id: int):
    return await delete_user_student_util(student_id)
