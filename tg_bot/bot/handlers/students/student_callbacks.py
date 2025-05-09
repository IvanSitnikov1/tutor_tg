"""Модуль содержит callback функции для учеников"""

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.functions.lessons.lesson_funcs import show_lesson_for_student_details, pre_upload_file
from bot.routers import student_router
from bot.storage import STUDENTS
from loggers import logger


@student_router.callback_query(
    lambda c: c.data.startswith('show_lesson:') and c.from_user.id in STUDENTS,
)
async def show_lesson(call: CallbackQuery):
    """Функция обрабатывает нажатие на конкретный урок, отображает урок для ученика"""

    lesson_id = call.data.split(':')[1]
    logger.info(f'Получен запрос на отображение урока с id {lesson_id}')
    await show_lesson_for_student_details(call.message, lesson_id)


@student_router.callback_query(lambda c: c.data.startswith('add_solution:'))
async def add_solution(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие на кнопку добавления решения, добавляет файл с решением задания"""

    logger.info('Получен запрос на добавление файла с решением задания')
    await pre_upload_file(call, state, "solutions")
