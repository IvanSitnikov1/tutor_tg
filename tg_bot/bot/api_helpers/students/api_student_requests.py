from bot.api_helpers.request_decorator import request_decorator
from config import API_URL


@request_decorator
async def get_students_list_tg_id():
    url = f'{API_URL}/users/students/list_tg_id'
    return url, 'GET', None, 200


@request_decorator
async def get_student_request(student_tg_id):
    url = f'{API_URL}/users/students/student/tg_id/{student_tg_id}'
    return url, 'GET', None, 200


@request_decorator
async def upload_solution_in_lesson_request(author_id, lesson_id, file_name):
    url = f'{API_URL}/lessons/completed_homeworks'
    data = {
        'author_id': author_id,
        'lesson_id': lesson_id,
        'file_path': f'/solutions/{file_name}',
    }
    return url, 'POST', data, 200
