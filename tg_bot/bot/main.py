import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_TOKEN
from bot.handlers import auth_router, teacher_router


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(auth_router)
dp.include_router(teacher_router)


async def start_bot():
    await dp.start_polling(bot)
