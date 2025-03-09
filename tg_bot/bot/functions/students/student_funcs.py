from aiogram.types import Message

from bot.keyboards.student_keyboards import student_menu_kb


async def show_student_menu(message: Message):
    """Отображает меню студента."""
    await message.answer("Меню", reply_markup=student_menu_kb())
