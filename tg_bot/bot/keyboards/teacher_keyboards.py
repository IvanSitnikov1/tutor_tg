from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup


def teacher_menu_kb():
    kb_list = [
        [KeyboardButton(text='👤Ученики')], [KeyboardButton(text='📝Личные файлы')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def students_kb(students):
    kb_list = []
    for student in students:
        student_name = student.get('username')
        kb_list.append([InlineKeyboardButton(
            text=student_name, callback_data=f'show_lessons_of_student:{student.get('id')}')]
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def lessons_of_student_kb(student):
    kb_list = []
    for lesson in student.get('lessons'):
        lesson_button = InlineKeyboardButton(
            text=f'{'✅' if lesson.get('is_done') else ''}{lesson.get('name')}',
            callback_data=f'show_lesson:{lesson.get('id')}:{student.get('id')}'
        )
        delete_button = InlineKeyboardButton(
            text='🗑 Delete',
            callback_data=f'delete_lesson:{lesson.get('id')}',
        )
        kb_list.append([lesson_button, delete_button])

    kb_list.append([InlineKeyboardButton(
        text='➕ Add lesson',
        callback_data=f'add_lesson:{student.get('id')}')],
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def lesson_files_kb(lesson_id, file_type):
    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_lesson_file:{lesson_id}')],
        [InlineKeyboardButton(text='Delete all', callback_data=f'delete_all_lesson_files:{lesson_id}'),
        InlineKeyboardButton(text='Delete multiple', callback_data=f'delete_lesson_files:{lesson_id}:{file_type}')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def lesson_homework_kb(lesson_id, file_type):
    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_lesson_homework:{lesson_id}')],
        [InlineKeyboardButton(text='Delete all', callback_data=f'delete_all_lesson_homeworks:{lesson_id}'),
        InlineKeyboardButton(text='Delete multiple', callback_data=f'delete_lesson_files:{lesson_id}:{file_type}')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def personal_files_kb(user_id):
    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_personal_file:{user_id}')],
        [InlineKeyboardButton(text='Delete all', callback_data=f'delete_all_personal_files:{user_id}'),
        InlineKeyboardButton(text='Delete multiple', callback_data=f'pre_delete_personal_files')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def toggle_lesson_is_done_kb(lesson):
    kb_list = [
        [InlineKeyboardButton(
            text=f'{'✅' if lesson.get('is_done') else lesson.get('name')}',
            callback_data=f'toggle_lesson_is_done:{lesson.get('id')}',
        )]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
#
#
# def delete_files_kb(lesson, selected_files, file_type):
#     kb_list = []
#     for file in lesson[file_type]:
#         is_selected = selected_files.get(str(file['id']), False)
#         checkbox = '✅' if is_selected else ''
#         file_button = InlineKeyboardButton(text=f'{checkbox} {file['file_path']}', callback_data=f"toggle_file:{file['id']}:{lesson['id']}:{file_type}")
#         kb_list.append([file_button])
#     kb_list.append([InlineKeyboardButton(text="Удалить выбранное", callback_data=f'delete_selected_files:{lesson['id']}:{file_type}')])
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
#     return keyboard
#
#
def delete_personal_files_by_ids_kb(user, selected_files):
    kb_list = []
    for file in user.get('personal_files'):
        is_selected = selected_files.get(str(file.get('id')), False)
        checkbox = '✅' if is_selected else ''
        file_button = InlineKeyboardButton(
            text=f'{checkbox} {file.get('file_path').split('/')[-1]}',
            callback_data=f"toggle_personal_file:{file.get('id')}",
        )
        kb_list.append([file_button])
    kb_list.append([InlineKeyboardButton(text="Удалить выбранное", callback_data=f'delete_selected_personal_files')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def add_comment_kb(lesson_id):
    kb_list = [[InlineKeyboardButton(text='Добавить комментарий', callback_data=f'add_lesson_comment:{lesson_id}')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
