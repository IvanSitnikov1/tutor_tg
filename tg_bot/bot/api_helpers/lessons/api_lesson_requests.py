from config import API_URL
from bot.api_helpers.request_decorator import request_decorator


@request_decorator
async def get_lesson_request(lesson_id):
    url = f'{API_URL}/lessons/{lesson_id}'
    return url, 'GET', None


@request_decorator
async def add_lesson_request(author_id, student_id, lesson_name):
    url = f'{API_URL}/lessons'
    data = {
        'author_id': author_id,
        'student_id': student_id,
        'name': lesson_name,
    }
    return url, 'POST', data


@request_decorator
async def delete_lesson_request(lesson_id):
    url = f'{API_URL}/lessons/{lesson_id}'
    return url, 'DELETE', None


@request_decorator
async def upload_file_in_lesson_request(lesson_id, file_name):
    url = f'{API_URL}/lessons/files'
    data = {
        'lesson_id': lesson_id,
        'file_path': f'/files/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def upload_homework_in_lesson_request(lesson_id, file_name):
    url = f'{API_URL}/lessons/homeworks'
    data = {
        'lesson_id': lesson_id,
        'file_path': f'/homeworks/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def upload_comments_in_lesson_request(lesson_id, file_name):
    url = f'{API_URL}/lessons/comments_to_completed_homeworks'
    data = {
        'lesson_id': lesson_id,
        'file_path': f'/comments/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def upload_solution_in_lesson_request(lesson_id, file_name):
    url = f'{API_URL}/lessons/completed_homeworks'
    data = {
        'lesson_id': lesson_id,
        'file_path': f'/solutions/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def toggle_lesson_is_done_request(lesson_id):
    url = f'{API_URL}/lessons/{lesson_id}/change_is_done'
    return url, 'GET', None


@request_decorator
async def delete_files_in_lesson_request(files_ids):
    url = f'{API_URL}/lessons/files'
    data = {'files_ids': files_ids}
    return url, 'DELETE', data


@request_decorator
async def delete_homeworks_in_lesson_request(homeworks_ids):
    url = f'{API_URL}/lessons/homeworks'
    data = {'files_ids': homeworks_ids}
    return url, 'DELETE', data


@request_decorator
async def delete_all_files_requests(lesson_id, file_type):
    url = f'{API_URL}/lessons/{lesson_id}/{file_type}'
    return url, 'DELETE', None
