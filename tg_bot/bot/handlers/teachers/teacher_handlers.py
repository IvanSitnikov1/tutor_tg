import os

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.api_helpers.students.api_student_requests import upload_solution_in_lesson_request
from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request, \
    add_lesson_request, upload_file_in_lesson_request, upload_homework_in_lesson_request, upload_personal_file_request, \
    upload_comments_in_lesson_request
from bot.contexts import UploadFile
from bot.functions import show_teacher_menu, show_personal_files, show_lesson_details, show_lesson_by_student_details
from bot.keyboards.inline_keyboards import students_kb
from bot.routers import teacher_router


@teacher_router.message(F.text)
async def handle_teacher_message(message: Message, state: FSMContext):
    if message.text == 'Меню':
        await show_teacher_menu(message)
    elif message.text == '👤Ученики':
        current_user = await get_teacher_request(message.from_user.id)
        await message.answer('Ваши студенты:', reply_markup=students_kb(current_user['students']))
    elif message.text == '📝Личные файлы':
        await show_personal_files(message)
    else:
        await state.update_data(lesson_name=message.text)
        lesson_data = await state.get_data()
        new_lesson = await add_lesson_request(lesson_data['student_id'], lesson_data['lesson_name'])
        if new_lesson:
            await message.answer("Урок добавлен успешно")
            await show_lesson_details(message, new_lesson['id'])
        else:
            await message.answer("Не получилось добавить урок")
    await state.clear()


@teacher_router.message(lambda message: message.document or message.photo, UploadFile.file)
async def handle_upload_file(message: Message, state: FSMContext):
    file = None
    file_name = None
    if message.document:
        file = message.document
        file_name = file.file_name
    if message.photo:
        file = message.photo[-1]
        file_name = f'{file.file_id}.jpg'

    state_data = await state.get_data()
    file_path = os.path.join(f'/home/ivan/Projects/tutor_tg/static/{state_data['file_type']}', file_name)

    file_info = await message.bot.get_file(file.file_id)
    await message.bot.download_file(file_info.file_path, file_path)

    if state_data['file_type'] == 'files':
        link_file = await upload_file_in_lesson_request(state_data['author_id'], state_data['lesson_id'], file_name)
    elif state_data['file_type'] == 'homeworks':
        link_file = await upload_homework_in_lesson_request(state_data['author_id'], state_data['lesson_id'], file_name)
    elif state_data['file_type'] == 'solutions':
        link_file = await upload_solution_in_lesson_request(state_data['author_id'], state_data['lesson_id'], file_name)
    elif state_data['file_type'] == 'comments':
        link_file = await upload_comments_in_lesson_request(state_data['author_id'], state_data['lesson_id'], file_name)
    else:
        link_file = await upload_personal_file_request(state_data['author_id'], file_name)

    if link_file:
        await message.answer('Файл успешно загружен')
        if state_data['file_type'] in ['solutions', 'comments']:
            await show_lesson_by_student_details(message, state_data['lesson_id'])
        elif state_data['file_type'] in ['files', 'homeworks']:
            await show_lesson_details(message, state_data['lesson_id'])
        elif state_data['file_type'] == 'personal':
            await show_personal_files(message)
    else:
        await message.answer("❌ Не удалось загрузить файл.")
    await state.clear()
