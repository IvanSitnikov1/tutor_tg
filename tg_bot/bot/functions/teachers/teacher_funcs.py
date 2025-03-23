from aiogram.types import Message, FSInputFile

from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request
from bot.keyboards.teacher_keyboards import teacher_menu_kb, personal_files_kb
from config import STATIC_URL


async def show_teacher_menu(message: Message):
    """Отображает меню учителя."""
    await message.answer("Меню", reply_markup=teacher_menu_kb())


async def send_media(message, file, reply_markup=None):
    if file.path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        await message.answer_photo(photo=file, reply_markup=reply_markup)
    elif file.path.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
        await message.answer_video(video=file, reply_markup=reply_markup)
    elif file.path.endswith(('.mp3', '.wav', '.ogg', '.flac', '.aac')):
        await message.answer_audio(audio=file, reply_markup=reply_markup)


async def show_personal_files(message: Message):
    current_user = await get_teacher_request(message.from_user.id)

    material_files_media = []
    files_text = '<b>Файлы</b>\n'
    for personal_file in current_user.get('data', {}).get('personal_files', []):
        file_url = (f"<a href='{STATIC_URL}{personal_file.get('file_path')}'>"
                    f"{personal_file.get('file_path').split('/')[-1]}</a>")

        if personal_file.get('file_path').endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp',
                                                   '.mp4', '.mov', '.avi', '.mkv', '.webm',
                                                   '.mp3', '.wav', '.ogg', '.flac', '.aac')):
            file_fs = FSInputFile(f'/home/ivan/Projects/tutor_tg/static{personal_file.get("file_path")}')
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
