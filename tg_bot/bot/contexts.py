"""Модуль содержит классы контекстов, используемых в боте"""

from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    """Контекст для регистрации пользователя в боте"""

    username = State()
    user_type = State()
    teacher_id = State()


class AddLesson(StatesGroup):
    """Контекст для добавления урока"""

    student_id = State()
    lesson_name = State()


class EditLessonDate(StatesGroup):
    """Контекст для редактирования даты урока"""

    lesson_id = State()
    new_date = State()


class UploadFile(StatesGroup):
    """
    Контекст для загрузки файлов материалов, домашних заданий, выполненных
    домашних заданий, комментариев к домашним заданиям и личных файлов
    """

    author_id = State()
    lesson_id = State()
    file = State()
    file_type = State()
    file_name = State()


class SelectedFiles(StatesGroup):
    """Контекст для хранения выбранных файлов. Используется при выборочном удалении материалов и личных файлов"""

    selected_files = State()
