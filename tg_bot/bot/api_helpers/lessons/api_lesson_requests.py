"""Модуль содержит функции для выполнения запросов к API, связанных с уроками"""
from config import API_URL
from bot.api_helpers.request_decorator import request_decorator


@request_decorator
async def get_lesson_request(lesson_id):
    """Получение урока по id"""
    url = f'{API_URL}/lessons/{lesson_id}'
    return url, 'GET', None


@request_decorator
async def add_lesson_request(author_id, student_id, lesson_name):
    """Создание урока"""
    url = f'{API_URL}/lessons'
    data = {
        'author_id': author_id,
        'student_id': student_id,
        'name': lesson_name,
    }
    return url, 'POST', data


@request_decorator
async def delete_lesson_request(lesson_id):
    """Удаление урока по id"""
    url = f'{API_URL}/lessons/{lesson_id}'
    return url, 'DELETE', None


@request_decorator
async def upload_file_in_lesson_request(lesson_id, file_name):
    """Добавление материала к уроку"""
    url = f'{API_URL}/lessons/files'
    data = {
        'lesson_id': lesson_id,
        'file_path': f'/files/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def upload_homework_in_lesson_request(lesson_id, file_name):
    """Добавление домашнего задания к уроку"""
    url = f'{API_URL}/lessons/homeworks'
    data = {
        'lesson_id': lesson_id,
        'file_path': f'/homeworks/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def upload_comments_in_lesson_request(lesson_id, file_name):
    """ДОбавление комментария в выполненному домашнему заданию урока"""
    url = f'{API_URL}/lessons/comments_to_completed_homeworks'
    data = {
        'lesson_id': lesson_id,
        'file_path': f'/comments/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def upload_solution_in_lesson_request(lesson_id, file_name):
    """Добавление решения к домашнему заданию урока"""
    url = f'{API_URL}/lessons/completed_homeworks'
    data = {
        'lesson_id': lesson_id,
        'file_path': f'/solutions/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def toggle_lesson_is_done_request(lesson_id):
    """Смена статуса урока(выполнен/не выполнен)"""
    url = f'{API_URL}/lessons/{lesson_id}/change_is_done'
    return url, 'GET', None


@request_decorator
async def delete_files_in_lesson_request(files_ids):
    """Удаление материалов из урока по списку id материалов"""
    url = f'{API_URL}/lessons/files'
    data = {'files_ids': files_ids}
    return url, 'DELETE', data


@request_decorator
async def delete_homeworks_in_lesson_request(homeworks_ids):
    """Удаление домашних заданий из урока по списку id домашних заданий"""
    url = f'{API_URL}/lessons/homeworks'
    data = {'files_ids': homeworks_ids}
    return url, 'DELETE', data


@request_decorator
async def delete_all_files_requests(lesson_id, file_type):
    """Удаление всех файлов лекции определенного типа"""
    url = f'{API_URL}/lessons/{lesson_id}/{file_type}'
    return url, 'DELETE', None


@request_decorator
async def update_lesson_date_requests(lesson_id, new_date):
    """Изменение даты урока"""
    url = f'{API_URL}/lessons/{lesson_id}?new_date={new_date}'
    return url, 'PUT', None
