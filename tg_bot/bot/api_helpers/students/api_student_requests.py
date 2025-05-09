"""Модуль содержит функции для выполнения запросов к API, связанных с учениками"""
from bot.api_helpers.request_decorator import request_decorator
from config import API_URL


@request_decorator
async def create_student_request(username: str, student_id: int, teacher_id: int):
    """Создает пользователя ученика"""
    url = f'{API_URL}/students'
    data = {
        'username': username,
        'id': student_id,
        'teacher_id': teacher_id,
    }
    return url, 'POST', data


@request_decorator
async def get_student_request(student_id):
    """Получает пользователя ученика по id"""
    url = f'{API_URL}/students/{student_id}'
    return url, 'GET', None


@request_decorator
async def get_students_list_ids_request():
    """Получает список id всех студентов"""
    url = f'{API_URL}/students'
    return url, 'GET', None


@request_decorator
async def delete_student_request(student_id):
    """Удаляет пользователя студента"""
    url = f'{API_URL}/students/{student_id}'
    return url, 'DELETE', None
