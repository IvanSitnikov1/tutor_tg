from config import API_URL
from bot.api_helpers.request_decorator import request_decorator


@request_decorator
async def get_teacher_with_students_request(teacher_tg_id):
    url = f'{API_URL}/users/get_teacher_for_tg_id?teacher_tg_id={teacher_tg_id}'
    return url, 'GET', None, 200


@request_decorator
async def get_student_request(student_id):
    url = f'{API_URL}/users/get_student_for_id?student_id={student_id}'
    return url, 'GET', None, 200


@request_decorator
async def get_lesson_request(lesson_id):
    url = f'{API_URL}/lessons/get_lesson_for_id?lesson_id={lesson_id}'
    return url, 'GET', None, 200


@request_decorator
async def add_lesson_request(student_id, lesson_name):
    url = f'{API_URL}/lessons/add_lesson'
    data = {
        'student_id': student_id,
        'name': lesson_name,
    }
    return url, 'POST', data, 200


@request_decorator
async def delete_lesson_request(lesson_id):
    url = f'{API_URL}/lessons/delete_lesson?lesson_id={lesson_id}'
    return url, 'DELETE', None, 200


@request_decorator
async def upload_file_in_lesson(author_id, lesson_id, file_name):
    url = f'{API_URL}/lessons/add_file_in_lesson'
    data = {
        'author_id': author_id,
        'lesson_id': lesson_id,
        'file_path': f'/files/{file_name}',
    }
    return url, 'POST', data, 200


@request_decorator
async def upload_homework(author_id, lesson_id, file_name):
    url = f'{API_URL}/lessons/add_homework'
    data = {
        'author_id': author_id,
        'lesson_id': lesson_id,
        'file_path': f'/homeworks/{file_name}',
    }
    return url, 'POST', data, 200


@request_decorator
async def upload_personal_file(author_id, file_name):
    url = f'{API_URL}/users/add_personal_file'
    data = {
        'author_id': author_id,
        'file_path': f'/personal/{file_name}',
    }
    return url, 'POST', data, 200
