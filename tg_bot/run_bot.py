import asyncio
import os

from bot.main import dp, bot
from bot.storage import update_students
from bot.handlers import auth_router, teacher_router, student_router


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


if __name__ == '__main__':
    asyncio.run(start_bot())
