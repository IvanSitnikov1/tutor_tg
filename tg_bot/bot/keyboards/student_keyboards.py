


def student_menu_kb():
    kb_list = [[KeyboardButton(text='📒Уроки')]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
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
