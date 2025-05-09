"""Модуль содержит функции для выполнения запросов к API, связанных с учителями"""
from config import API_URL
from bot.api_helpers.request_decorator import request_decorator


@request_decorator
async def create_teacher_request(username: str, teacher_id: int):
    """Создает пользователя учителя"""
    url = f'{API_URL}/teachers'
    data = {
        'username': username,
        'id': teacher_id,
    }
    return url, 'POST', data


@request_decorator
async def get_teacher_request(teacher_id):
    """Получает пользователя учителя по id"""
    url = f'{API_URL}/teachers/{teacher_id}'
    return url, 'GET', None


@request_decorator
async def upload_personal_file_request(author_id, file_name):
    """Добавляет личный файл учителя"""
    url = f'{API_URL}/teachers/personal_files'
    data = {
        'author_id': author_id,
        'file_path': f'/personal/{file_name}',
    }
    return url, 'POST', data


@request_decorator
async def delete_personal_files_request(personal_files_ids):
    """Удаляет личный файл учителя"""
    url = f'{API_URL}/teachers/personal_files'
    data = {'files_ids': personal_files_ids}
    return url, 'DELETE', data
