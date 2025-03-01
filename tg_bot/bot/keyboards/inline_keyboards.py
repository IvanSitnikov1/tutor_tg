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


def student_detail_kb(student):
    kb_list = []
    for lesson in student['lessons']:
        lesson_button = InlineKeyboardButton(text=lesson['name'], callback_data=f'show_lesson:{lesson["id"]}:{student['id']}')
        delete_button = InlineKeyboardButton(text='🗑 Удалить', callback_data=f'delete_lesson:{lesson["id"]}')
        kb_list.append([lesson_button, delete_button])  # Располагаем кнопки в один ряд

    kb_list.append([InlineKeyboardButton(text='➕ Добавить урок', callback_data=f'add_lesson:{student['id']}')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def lesson_files_kb(lesson_id, file_type):
    kb_list = [[
        InlineKeyboardButton(text='Add', callback_data=f'add_lesson_file:{lesson_id}'),
        InlineKeyboardButton(text='Удалить все', callback_data=f'delete_all_lesson_files:{lesson_id}'),
        InlineKeyboardButton(text='Удалить выборочно', callback_data=f'delete_lesson_files:{lesson_id}:{file_type}'),
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def lesson_homework_kb(lesson_id, file_type):
    kb_list = [[
        InlineKeyboardButton(text='Add', callback_data=f'add_lesson_homework:{lesson_id}'),
        InlineKeyboardButton(text='Удалить все', callback_data=f'delete_all_lesson_homeworks:{lesson_id}'),
        InlineKeyboardButton(text='Удалить выборочно', callback_data=f'delete_lesson_files:{lesson_id}:{file_type}'),
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def personal_files_kb(user_id):
    kb_list = [[
        InlineKeyboardButton(text='Add', callback_data=f'add_personal_file:{user_id}'),
        InlineKeyboardButton(text='Удалить все', callback_data=f'delete_all_personal_files:{user_id}'),
        InlineKeyboardButton(text='Удалить выборочно', callback_data=f'delete_personal_files'),
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def toggle_lesson_is_done_kb(lesson):
    kb_list = [
        [InlineKeyboardButton(text=f'Урок {lesson['name']} {'✅' if lesson['is_done'] else ''}', callback_data=f'toggle_lesson_is_done:{lesson['id']}')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def delete_files_kb(lesson, selected_files, file_type):
    kb_list = []
    for file in lesson[file_type]:
        is_selected = selected_files.get(str(file['id']), False)
        checkbox = '✅' if is_selected else ''
        file_button = InlineKeyboardButton(text=f'{checkbox} {file['file_path']}', callback_data=f"toggle_file:{file['id']}:{lesson['id']}:{file_type}")
        kb_list.append([file_button])
    kb_list.append([InlineKeyboardButton(text="Удалить выбранное", callback_data=f'delete_selected_files:{lesson['id']}:{file_type}')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def delete_personal_files_kb(user, selected_files):
    kb_list = []
    for file in user['personal_files']:
        is_selected = selected_files.get(str(file['id']), False)
        checkbox = '✅' if is_selected else ''
        file_button = InlineKeyboardButton(text=f'{checkbox} {file['file_path']}', callback_data=f"toggle_personal_file:{file['id']}")
        kb_list.append([file_button])
    kb_list.append([InlineKeyboardButton(text="Удалить выбранное", callback_data=f'delete_selected_personal_files')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def show_lessons_student_kb(lessons):
    kb_list = []
    for lesson in lessons:
        kb_list.append([InlineKeyboardButton(
            text=lesson['name'], callback_data=f'show_lesson_student_detail:{lesson['id']}')]
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
        return keyboard


def add_solution_kb(lesson_id):
    kb_list = [[InlineKeyboardButton(text='Добавить решение', callback_data=f'add_lesson_solution:{lesson_id}')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def add_comment_kb(lesson_id):
    kb_list = [[InlineKeyboardButton(text='Добавить комментарий', callback_data=f'add_lesson_comment:{lesson_id}')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
