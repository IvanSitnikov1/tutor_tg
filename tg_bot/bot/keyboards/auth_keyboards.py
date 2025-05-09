"""Модуль содержит клавиатуры для регистрации пользователя"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def user_type_kb():
    """Клавиатура с выбором типа пользователя"""

    kb_list = [
        [InlineKeyboardButton(text="Teacher", callback_data='set_teacher')],
        [InlineKeyboardButton(text="Student", callback_data='set_student')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
