from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def user_type_kb():
    kb_list = [
        [InlineKeyboardButton(text="Teacher", callback_data='set_teacher')],
        [InlineKeyboardButton(text="Student", callback_data='set_student')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def students_kb(students):
    kb_list = []
    for student in students:
        student_name = student['username']
        kb_list.append([InlineKeyboardButton(
            text=student_name, callback_data=f'show_student:{student['id']}')]
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def student_detail_kb(lessons):
    kb_list = []
    student_id = lessons[0]['student_id']
    for lesson in lessons:
        lesson_button = InlineKeyboardButton(text=lesson['name'], callback_data=f'show_lesson:{lesson["id"]}:{student_id}')
        delete_button = InlineKeyboardButton(text='🗑 Удалить', callback_data=f'delete_lesson:{lesson["id"]}')
        kb_list.append([lesson_button, delete_button])  # Располагаем кнопки в один ряд

    kb_list.append([InlineKeyboardButton(text='➕ Добавить урок', callback_data=f'add_lesson:{student_id}')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def add_lesson_file_kb(lesson_id):
    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_lesson_file:{lesson_id}')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def add_lesson_homework_kb(lesson_id):
    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_lesson_homework:{lesson_id}')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def personal_files_kb(user_id):
    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_personal_file:{user_id}')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
