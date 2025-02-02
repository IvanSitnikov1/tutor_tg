from config import API_URL
from bot.api_helpers.request_decorator import request_decorator


@request_decorator
async def get_students_request(teacher_tg_id):
    url = f'{API_URL}/users/get_students_for_teacher?teacher_tg_id={teacher_tg_id}'
    return url, 'GET', None, 200


@request_decorator
async def get_student_request(student_id):
    url = f'{API_URL}/users/get_student_for_id?student_id={student_id}'
    return url, 'GET', None, 200


@request_decorator
async def get_lesson_request(lesson_id):
    url = f'{API_URL}/lessons/get_lesson_for_id?lesson_id={lesson_id}'
    return url, 'GET', None, 200
