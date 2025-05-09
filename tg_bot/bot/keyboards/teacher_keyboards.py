"""Модуль содержит клавиатуры для учителя"""

import calendar
from datetime import datetime, timedelta

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup


def teacher_menu_kb():
    """Клавиатура меню учителя"""

    kb_list = [
        [KeyboardButton(text='👤Ученики'), KeyboardButton(text='📩 Пригласить ученика')],
        [KeyboardButton(text='📝Личные файлы')],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def students_kb(students):
    """Клавиатура со списком учеников и кнопками удаления учеников"""

    kb_list = []
    for student in students:
        student_name = student.get('username')
        kb_list.append([
            InlineKeyboardButton(
                text=student_name, callback_data=f"show_lessons_of_student:{student.get('id')}"
            ),
            InlineKeyboardButton(
                text='🗑 Delete', callback_data=f"delete_student:{student.get('id')}"
            )
        ])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def lessons_of_student_kb(student):
    """Клавиатура показывает список уроков ученика с кнопками удаления. Последняя кнопка - добавление урока"""

    kb_list = []
    for lesson in student.get('lessons'):
        lesson_button = InlineKeyboardButton(
            text=f"{'✅' if lesson.get('is_done') else ''}{lesson.get('name')}",
            callback_data=f"show_lesson:{lesson.get('id')}:{student.get('id')}"
        )
        delete_button = InlineKeyboardButton(
            text='🗑 Delete',
            callback_data=f"delete_lesson:{lesson.get('id')}",
        )
        kb_list.append([lesson_button, delete_button])

    kb_list.append([InlineKeyboardButton(
        text='➕ Add lesson',
        callback_data=f"add_lesson:{student.get('id')}"
    )])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def lesson_files_kb(lesson_id, file_type):
    """Клавиатура отображает функциональные кнопки дабавления и двух типов удаления материалов урока"""

    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_lesson_file:{lesson_id}')],
        [InlineKeyboardButton(text='Delete all', callback_data=f'delete_all_lesson_files:{lesson_id}:{file_type}'),
        InlineKeyboardButton(text='Delete multiple', callback_data=f'delete_lesson_files:{lesson_id}:{file_type}')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def lesson_homework_kb(lesson_id, file_type):
    """Клавиатура отображает функциональные кнопки дабавления и двух типов удаления домашних заданий урока"""

    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_lesson_homework:{lesson_id}')],
        [InlineKeyboardButton(text='Delete all', callback_data=f'delete_all_lesson_files:{lesson_id}:{file_type}'),
        InlineKeyboardButton(text='Delete multiple', callback_data=f'delete_lesson_files:{lesson_id}:{file_type}')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def personal_files_kb(user_id):
    """Клавиатура отображает функциональные кнопки дабавления и двух типов удаления личных файлов"""

    kb_list = [
        [InlineKeyboardButton(text='Add', callback_data=f'add_personal_file:{user_id}')],
        [InlineKeyboardButton(text='Delete all', callback_data=f'delete_all_personal_files:{user_id}'),
        InlineKeyboardButton(text='Delete multiple', callback_data=f'pre_delete_personal_files')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def toggle_lesson_is_done_kb(lesson):
    """Клавиатура отображает название открытого урока в зависимости от его состояния и меняет это состояние"""

    kb_list = [
        [InlineKeyboardButton(
            text=f"{'✅' if lesson.get('is_done') else lesson.get('name')}",
            callback_data=f"toggle_lesson_is_done:{lesson.get('id')}",
        )]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def delete_files_kb(lesson, selected_files, file_type):
    """Клавиатура отображает файлы урока для удаления с соответствующем состоянии чекбокса, а так же кнопку удаления"""

    kb_list = []
    for file in lesson.get(file_type):
        is_selected = selected_files.get(str(file.get('id')), False)
        checkbox = '✅' if is_selected else ''
        file_button = InlineKeyboardButton(
            text=f"{checkbox} {file.get('file_path')}",
            callback_data=f"toggle_file:{file.get('id')}:{lesson.get('id')}:{file_type}",
        )
        kb_list.append([file_button])

    kb_list.append([InlineKeyboardButton(
        text="Delete files",
        callback_data=f"delete_selected_files:{lesson.get('id')}:{file_type}"
    )])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def delete_personal_files_by_ids_kb(user, selected_files):
    """Клавиатура отображает личные файлы для удаления с соответствующем состоянии чекбокса, а так же кнопку удаления"""

    kb_list = []
    for file in user.get('personal_files'):
        is_selected = selected_files.get(str(file.get('id')), False)
        checkbox = '✅' if is_selected else ''
        file_button = InlineKeyboardButton(
            text=f"{checkbox} {file.get('file_path').split('/')[-1]}",
            callback_data=f"toggle_personal_file:{file.get('id')}",
        )
        kb_list.append([file_button])
    kb_list.append([InlineKeyboardButton(text="Delete files", callback_data=f'delete_selected_personal_files')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def add_comment_kb(lesson_id):
    """Клавиатура отображает кнопку для добавления комментария к домашнему заданию урока"""

    kb_list = [[InlineKeyboardButton(text='Add comment', callback_data=f'add_lesson_comment:{lesson_id}')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def generate_calendar(year, month):
    """Клавиатура генерирует календарь для выбота даты урока"""

    keyboard = []

    month_name = calendar.month_name[month]
    keyboard.append([InlineKeyboardButton(text=f"📅 {month_name} {year}", callback_data="ignore")])

    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    keyboard.append([InlineKeyboardButton(text=day, callback_data="ignore") for day in days])

    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))  # Пустые клетки
            else:
                date_str = f"{day:02d}-{month:02d}-{year}"
                row.append(InlineKeyboardButton(text=str(day), callback_data=f"select_date_{date_str}"))
        keyboard.append(row)

    prev_month = (datetime(year, month, 1) - timedelta(days=1)).month
    prev_year = (datetime(year, month, 1) - timedelta(days=1)).year

    next_month = (datetime(year, month, 28) + timedelta(days=4)).month
    next_year = (datetime(year, month, 28) + timedelta(days=4)).year

    keyboard.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data=f"change_month_{prev_year}_{prev_month}"),
        InlineKeyboardButton(text="➡️ Вперёд", callback_data=f"change_month_{next_year}_{next_month}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
