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
    for lesson in lessons:
        kb_list.append([InlineKeyboardButton(text=lesson['name'], callback_data=f'show_lesson:{lesson['id']}')])
    kb_list.append([InlineKeyboardButton(text='Добавить урок', callback_data='gfdsg')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def add_lesson_kb():
    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data='add')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def add_homework_kb():
    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data='add')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
