from aiogram.types import Message

from bot.keyboards.reply_reyboards import teacher_menu_kb, student_menu_kb


async def teacher_menu(message: Message):
    """Отображает меню учителя."""
    await message.answer("Меню", reply_markup=teacher_menu_kb())

async def student_menu(message: Message):
    """Отображает меню студента."""
    await message.answer("Меню", reply_markup=student_menu_kb())
