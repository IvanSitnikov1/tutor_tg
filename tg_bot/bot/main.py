import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.storage import update_students
from config import TELEGRAM_TOKEN
from bot.handlers import auth_router, teacher_router, student_router


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


def create_dirs_statis():
    os.makedirs('../static', exist_ok=True)
    os.makedirs('../static/files', exist_ok=True)
    os.makedirs('../static/homeworks', exist_ok=True)
    os.makedirs('../static/comments', exist_ok=True)
    os.makedirs('../static/personal', exist_ok=True)
    os.makedirs('../static/solutions', exist_ok=True)


async def start_bot():
    create_dirs_statis()
    await update_students()
    dp.include_router(auth_router)
    dp.include_router(teacher_router)
    dp.include_router(student_router)
    await dp.start_polling(bot)
