import os

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
from config import STATIC_URL


async def upload_file_on_server(message: Message, state: FSMContext):
    file = None
    file_name = None

    if message.document:
        file = message.document
        file_name = file.file_name
    elif message.photo:
        file = message.photo[-1]
        file_name = f'{file.file_id}.jpg'
    elif message.video:
        file = message.video
        file_name = f'{file.file_id}.mp4'
    elif message.audio:
        file = message.audio
        file_name = f'{file.file_id}.mp3'

    if not file:
        await message.answer("Файл не найден или формат не поддерживается.")
        return

    await state.update_data(file_name=file_name)
    state_data = await state.get_data()

    file_type = state_data.get('file_type')
    file_path = os.path.join(f'/home/ivan/Projects/tutor_tg/static/{file_type}', file_name)

    file_info = await message.bot.get_file(file.file_id)
    await message.bot.download_file(file_info.file_path, file_path)


async def save_file_in_db(state):
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
    lesson_id = call.data.split(':')[1]

    await state.clear()
    await state.update_data(file_type=file_type, lesson_id=lesson_id)
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)


async def show_files_by_type(files, file_type):
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
            file_fs = FSInputFile(f'/home/ivan/Projects/tutor_tg/static{file_path}')
            media.append(file_fs)
        else:
            text += f"{file_url}\n--------\n"

    return media, text


async def send_media(message, file, reply_markup=None):
    if file.path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        await message.answer_photo(photo=file, reply_markup=reply_markup)
    elif file.path.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
        await message.answer_video(video=file, reply_markup=reply_markup)
    elif file.path.endswith(('.mp3', '.wav', '.ogg', '.flac', '.aac')):
        await message.answer_audio(audio=file, reply_markup=reply_markup)


async def show_lesson_for_student_details(message, lesson_id):
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

    await message.answer(comments_to_completed_homeworks_text, parse_mode='HTML')
    if comments_to_completed_homework_media:
        for file in comments_to_completed_homework_media[:-1]:
            await send_media(message, file)
        await send_media(
            message,
            comments_to_completed_homework_media[-1],
            reply_markup=add_solution_kb(lesson_id),
        )


async def show_lesson_for_teacher_details(message, lesson_id):
    lesson = await get_lesson_request(lesson_id)
    await message.answer("📒", reply_markup=toggle_lesson_is_done_kb(lesson.get('data', {})))

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
