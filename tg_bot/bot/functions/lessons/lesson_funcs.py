"""Модуль содержит функции для работы с уроками"""

import os
import random
import string

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot.api_helpers.lessons.api_lesson_requests import upload_file_in_lesson_request, \
    upload_homework_in_lesson_request, upload_solution_in_lesson_request, \
    upload_comments_in_lesson_request, get_lesson_request
from bot.api_helpers.teachers.api_teacher_requests import upload_personal_file_request
from bot.contexts import UploadFile
from bot.keyboards.student_keyboards import add_solution_kb
from bot.keyboards.teacher_keyboards import toggle_lesson_is_done_kb, lesson_files_kb, \
    lesson_homework_kb, add_comment_kb
from config import STATIC_URL, STATIC_PATH, BOT_NAME


def generate_random_string(length=4):
    """Функция генерирует рандомный префикс для названия файла, что б решить проблему уникальности названий"""

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def upload_file_on_server(message: Message, state: FSMContext):
    """Функция обрабатывает файл из сообщения, генерирует имя файла и сохраняет файл на сервере"""

    file = None
    file_name = None

    random_str = generate_random_string()

    # В зависимости от типа файла генерируем имя
    if message.document:
        file = message.document
        file_name = f"{random_str}_{file.file_name}"
    elif message.photo:
        file = message.photo[-1]
        file_name = f"{file.file_id}_{random_str}.jpg"
    elif message.video:
        file = message.video
        file_name = f"{file.file_id}_{random_str}.mp4"
    elif message.audio:
        file = message.audio
        file_name = f"{file.file_id}_{random_str}.mp3"

    if not file:
        return 'Неизвестный формат файла'

    # Обрабатывает максимальный размер файла согласно API Telegram
    if file.file_size > 20 * 1024 * 1024:
        return 'Превышен допустимый размер файла - 20 Мб'

    await state.update_data(file_name=file_name)
    state_data = await state.get_data()

    # Формируем путь к файлу на сервере
    file_type = state_data.get('file_type')
    file_path = os.path.join(f'{STATIC_PATH}{file_type}', file_name)

    # Загружаем файл на сервер
    file_info = await message.bot.get_file(file.file_id)
    await message.bot.download_file(file_info.file_path, file_path)


async def save_file_in_db(state):
    """Функция сохраняет загруженный файл в базе данных в зависимости от типа файла"""

    state_data = await state.get_data()

    if state_data.get('file_type') == 'files':
        return await upload_file_in_lesson_request(state_data.get('lesson_id'), state_data.get('file_name'))
    elif state_data.get('file_type') == 'homeworks':
        return await upload_homework_in_lesson_request(state_data.get('lesson_id'), state_data.get('file_name'))
    elif state_data.get('file_type') == 'solutions':
        return await upload_solution_in_lesson_request(state_data.get('lesson_id'), state_data.get('file_name'))
    elif state_data.get('file_type') == 'comments':
        return await upload_comments_in_lesson_request(state_data.get('lesson_id'), state_data.get('file_name'))
    else:
        return await upload_personal_file_request(state_data.get('author_id'), state_data.get('file_name'))


async def pre_upload_file(call: CallbackQuery, state: FSMContext, file_type: str):
    """
    Функция подготавливает контекст для загрузки файла, сохраняет в нем id урока и тип файла.
    Перенаправляет в состояние загрузки файла (handle_upload_file)
    """

    lesson_id = call.data.split(':')[1]

    await state.clear()
    await state.update_data(file_type=file_type, lesson_id=lesson_id)
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)


async def show_files_by_type(files, file_type):
    """Функция формирует текст и файлы для отображения в уроке в зависимости от типа файла"""

    media = []
    text = ''
    if file_type == 'files':
        text = '<b>Материалы</b>\n'
    elif file_type == 'homeworks':
        text = '<b>Домашние задания</b>\n'
    elif file_type == 'completed_homeworks':
        text = '<b>Выполненные задания</b>\n'
    elif file_type == 'comments_to_completed_homeworks':
        text = '<b>Комментарии учителя</b>\n'

    for file in files:
        file_path = file.get('file_path')
        file_url = (f"<a href='{STATIC_URL}{file_path}'>"
                    f"{file_path.split('/')[-1]}</a>")
        if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp',
                               '.mp4', '.mov', '.avi', '.mkv', '.webm',
                               '.mp3', '.wav', '.ogg', '.flac', '.aac')):
            file_fs = FSInputFile(f'{STATIC_PATH}{file_path}')
            media.append(file_fs)
        else:
            text += f"{file_url}\n--------\n"

    return media, text


async def send_media(message, file, reply_markup=None):
    """Функция отправляет в чат медиа файлы и клавиатуру после них (опционально)"""

    if file.path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        await message.answer_photo(photo=file, reply_markup=reply_markup)
    elif file.path.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
        await message.answer_video(video=file, reply_markup=reply_markup)
    elif file.path.endswith(('.mp3', '.wav', '.ogg', '.flac', '.aac')):
        await message.answer_audio(audio=file, reply_markup=reply_markup)


async def show_lesson_for_student_details(message, lesson_id):
    """
    Функция отображает урок и материалы для ученика. Сначала отображаются документы в виде ссылок,
    затем медиафайлы отправляются в чат, затем прикрепляется клавиатура для работы с файлами
    """

    lesson = await get_lesson_request(lesson_id)

    material_files_media, materials_text = await show_files_by_type(
        lesson.get('data', {}).get('files'),
        'files',
    )

    homework_media, homeworks_text = await show_files_by_type(
        lesson.get('data', {}).get('homeworks'),
        'homeworks',
    )

    completed_homework_media, completed_homeworks_text = await show_files_by_type(
        lesson.get('data', {}).get('completed_homeworks'),
        'completed_homeworks',
    )

    comments_to_completed_homework_media, comments_to_completed_homeworks_text = await show_files_by_type(
        lesson.get('data', {}).get('comments_to_completed_homeworks'),
        'comments_to_completed_homeworks',
    )

    await message.answer(materials_text, parse_mode='HTML')
    if material_files_media:
        for file in material_files_media[:-1]:
            await send_media(message, file)
        await send_media(message, material_files_media[-1])

    await message.answer(homeworks_text, parse_mode='HTML')
    if homework_media:
        for file in homework_media[:-1]:
            await send_media(message, file)
        await send_media(message, homework_media[-1])

    await message.answer(completed_homeworks_text, parse_mode='HTML')
    if completed_homework_media:
        for file in completed_homework_media[:-1]:
            await send_media(message, file)
        await send_media(message, completed_homework_media[-1])

    if comments_to_completed_homework_media:
        await message.answer(comments_to_completed_homeworks_text, parse_mode='HTML')
        for file in comments_to_completed_homework_media[:-1]:
            await send_media(message, file)
        await send_media(
            message,
            comments_to_completed_homework_media[-1],
            reply_markup=add_solution_kb(lesson_id),
        )
    else:
        await message.answer(
            comments_to_completed_homeworks_text, reply_markup=add_solution_kb(lesson_id), parse_mode='HTML'
        )


async def show_lesson_for_teacher_details(message, lesson_id):
    """
    Функция отображает урок и материалы для учителя. Сначала отображаются документы в виде ссылок,
    затем медиафайлы отправляются в чат, затем прикрепляется клавиатура для работы с файлами
    """

    lesson = await get_lesson_request(lesson_id)
    date = lesson.get('data', {}).get('date')
    year, month, day = date.split('-')
    # Отображаем название урока и дату с кнопкой редактирования даты (ссылается на обработчик комманды Start)
    await message.answer(
        f"📒 \\|{day}\\-{month}\\-{year}\\| [Edit](https://t.me/{BOT_NAME}?start=edit_date_{lesson_id})",
        reply_markup=toggle_lesson_is_done_kb(lesson.get('data', {})),
        parse_mode="MarkdownV2",
    )

    material_files_media, materials_text = await show_files_by_type(
        lesson.get('data', {}).get('files'),
        'files',
    )

    homework_media, homeworks_text = await show_files_by_type(
        lesson.get('data', {}).get('homeworks'),
        'homeworks',
    )

    completed_homework_media, completed_homeworks_text = await show_files_by_type(
        lesson.get('data', {}).get('completed_homeworks'),
        'completed_homeworks',
    )

    comments_to_completed_homework_media, comments_to_completed_homeworks_text = await show_files_by_type(
        lesson.get('data', {}).get('comments_to_completed_homeworks'),
        'comments_to_completed_homeworks',
    )

    if material_files_media:
        await message.answer(materials_text, parse_mode='HTML')
        for file in material_files_media[:-1]:
            await send_media(message, file)
        await send_media(
            message, material_files_media[-1], reply_markup=lesson_files_kb(lesson_id, 'files')
        )
    else:
        await message.answer(
            materials_text, reply_markup=lesson_files_kb(lesson_id, 'files'), parse_mode='HTML'
        )

    if homework_media:
        await message.answer(homeworks_text, parse_mode='HTML')
        for file in homework_media[:-1]:
            await send_media(message, file)
        await send_media(
            message, homework_media[-1], reply_markup=lesson_homework_kb(lesson_id, 'homeworks')
        )
    else:
        await message.answer(
            homeworks_text, reply_markup=lesson_homework_kb(lesson_id, 'homeworks'), parse_mode='HTML'
        )

    await message.answer(completed_homeworks_text, parse_mode='HTML')
    if completed_homework_media:
        for file in completed_homework_media[:-1]:
            await send_media(message, file)
        await send_media(message, completed_homework_media[-1])

    if comments_to_completed_homework_media:
        await message.answer(comments_to_completed_homeworks_text, parse_mode='HTML')
        for file in comments_to_completed_homework_media[:-1]:
            await send_media(message, file)
        await send_media(
            message,
            comments_to_completed_homework_media[-1],
            reply_markup=add_comment_kb(lesson_id),
        )
    else:
        await message.answer(
            comments_to_completed_homeworks_text, reply_markup=add_comment_kb(lesson_id), parse_mode='HTML'
        )
