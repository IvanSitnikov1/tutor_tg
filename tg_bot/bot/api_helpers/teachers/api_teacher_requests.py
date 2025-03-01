from config import API_URL
from bot.api_helpers.request_decorator import request_decorator


@request_decorator
async def get_teacher_request(teacher_tg_id):
    url = f'{API_URL}/users/teachers/teacher/{teacher_tg_id}'
    return url, 'GET', None, 200


@request_decorator
async def get_student_request(student_id):
    url = f'{API_URL}/users/students/student/{student_id}'
    return url, 'GET', None, 200


@request_decorator
async def get_lesson_request(lesson_id):
    url = f'{API_URL}/lessons/{lesson_id}'
    return url, 'GET', None, 200


@request_decorator
async def add_lesson_request(student_id, lesson_name):
    url = f'{API_URL}/lessons'
    data = {
        'student_id': student_id,
        'name': lesson_name,
    }
    return url, 'POST', data, 200


@request_decorator
async def delete_lesson_request(lesson_id):
    url = f'{API_URL}/lessons/lesson/{lesson_id}'
    return url, 'DELETE', None, 200


@request_decorator
async def upload_file_in_lesson_request(author_id, lesson_id, file_name):
    url = f'{API_URL}/lessons/files'
    data = {
        'author_id': author_id,
        'lesson_id': lesson_id,
        'file_path': f'/files/{file_name}',
    }
    return url, 'POST', data, 200


@request_decorator
async def upload_homework_in_lesson_request(author_id, lesson_id, file_name):
    url = f'{API_URL}/lessons/homeworks'
    data = {
        'author_id': author_id,
        'lesson_id': lesson_id,
        'file_path': f'/homeworks/{file_name}',
    }
    return url, 'POST', data, 200


@request_decorator
async def upload_comments_in_lesson_request(author_id, lesson_id, file_name):
    url = f'{API_URL}/lessons/comments_by_completed_homeworks'
    data = {
        'author_id': author_id,
        'lesson_id': lesson_id,
        'file_path': f'/comments/{file_name}',
    }
    return url, 'POST', data, 200


@request_decorator
async def upload_personal_file_request(author_id, file_name):
    url = f'{API_URL}/users/personal_files'
    data = {
        'author_id': author_id,
        'file_path': f'/personal/{file_name}',
    }
    return url, 'POST', data, 200


@request_decorator
async def toggle_lesson_is_done_request(lesson_id):
    url = f'{API_URL}/lessons/{lesson_id}/change_is_done'
    return url, 'GET', None, 200


@request_decorator
async def delete_files_in_lesson_request(files_ids):
    url = f'{API_URL}/lessons/files'
    data = {'files_ids': files_ids}
    return url, 'DELETE', data, 200


@request_decorator
async def delete_homeworks_in_lesson_request(homeworks_ids):
    url = f'{API_URL}/lessons/homeworks'
    data = {'files_ids': homeworks_ids}
    return url, 'DELETE', data, 200


@request_decorator
async def delete_personal_files_request(personal_files_ids):
    url = f'{API_URL}/users/files'
    data = {'files_ids': personal_files_ids}
    return url, 'DELETE', data, 200
