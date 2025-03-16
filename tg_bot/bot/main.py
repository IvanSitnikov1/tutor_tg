import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.api_helpers.students.api_student_requests import get_students_list_ids_request
from bot.storage import STUDENTS
from config import TELEGRAM_TOKEN
from bot.handlers import auth_router, teacher_router, student_router


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def update_students():
    global STUDENTS
    students = await get_students_list_ids_request()
    STUDENTS.clear()  # ✅ Очищает множество (ссылка остается)
    STUDENTS.update(students['data'])
    print("✅ Список пользователей обновлен:", STUDENTS)


async def start_bot():
    await update_students()
    dp.include_router(auth_router)
    dp.include_router(student_router)
    dp.include_router(teacher_router)
    await dp.start_polling(bot)
