from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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

def student_menu_kb():
    kb_list = [[KeyboardButton(text='📒Уроки')]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard
