"""Модуль содержит функции для работы с учителем"""

from aiogram.types import Message, FSInputFile

from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request
from bot.functions.lessons.lesson_funcs import send_media
from bot.keyboards.teacher_keyboards import teacher_menu_kb, personal_files_kb
from config import STATIC_URL, STATIC_PATH


async def show_teacher_menu(message: Message):
    """Отображает меню учителя."""

    await message.answer("Меню", reply_markup=teacher_menu_kb())


async def show_personal_files(message: Message):
    """
    Функция для отображения персональных файлов учителя. Отправляет фото, видео и аудио файлы в виде медиа файлов,
    документы и прочее в виде ссылки на статический файл.
    """

    current_user = await get_teacher_request(message.from_user.id)

    material_files_media = []
    files_text = '<b>Файлы</b>\n'
    for personal_file in current_user.get('data', {}).get('personal_files', []):
        file_url = (f"<a href='{STATIC_URL}{personal_file.get('file_path')}'>"
                    f"{personal_file.get('file_path').split('/')[-1]}</a>")

        if personal_file.get('file_path').endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp',
                                                   '.mp4', '.mov', '.avi', '.mkv', '.webm',
                                                   '.mp3', '.wav', '.ogg', '.flac', '.aac')):
            file_fs = FSInputFile(f'{STATIC_PATH}{personal_file.get("file_path")}')
            material_files_media.append(file_fs)
        else:
            files_text += f"{file_url}\n--------\n"

    if material_files_media:
        await message.answer(files_text, parse_mode='HTML')
        for file in material_files_media[:-1]:
            await send_media(message, file)
        await send_media(
            message,
            material_files_media[-1],
            reply_markup=personal_files_kb(current_user.get('data', {}).get('id')),
        )
    else:
        await message.answer(
            files_text,
            reply_markup=personal_files_kb(current_user.get('data', {}).get('id')),
            parse_mode='HTML',
        )
