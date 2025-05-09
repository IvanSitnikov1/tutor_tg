"""Модуль хранит список id студентов и функцию для его обновления"""
from bot.api_helpers.students.api_student_requests import get_students_list_ids_request
from loggers import logger

STUDENTS = set()


async def update_students():
    global STUDENTS
    students = await get_students_list_ids_request()
    STUDENTS.clear()  # ✅ Очищает множество (ссылка остается)
    STUDENTS.update(students['data'])
    logger.info(f"✅ Список учеников обновлен: {STUDENTS}")
