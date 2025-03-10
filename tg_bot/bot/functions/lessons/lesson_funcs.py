import os

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot.api_helpers.lessons.api_lesson_requests import upload_file_in_lesson_request, \
    upload_homework_in_lesson_request, upload_solution_in_lesson_request, \
    upload_comments_in_lesson_request, get_lesson_request
from bot.api_helpers.students.api_student_requests import get_student_request
from bot.api_helpers.teachers.api_teacher_requests import upload_personal_file_request, \
    get_teacher_request
from bot.contexts import UploadFile
from bot.keyboards.teacher_keyboards import toggle_lesson_is_done_kb, lesson_files_kb, \
    lesson_homework_kb, add_comment_kb
from config import STATIC_URL


async def upload_file_on_server(message: Message, state: FSMContext):
    file = None
    file_name = None
    if message.document:
        file = message.document
        file_name = file.file_name
    if message.photo:
        file = message.photo[-1]
        file_name = f'{file.file_id}.jpg'

    await state.update_data(file_name=file_name)
    state_data = await state.get_data()
    file_path = os.path.join(
        f'/home/ivan/Projects/tutor_tg/static/{state_data.get('file_type')}',
        file_name,
    )

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


# async def show_lesson_by_student_details(message, lesson_id):
#     lesson = await get_lesson_request(lesson_id)
#
#     material_files_image = []
#     materials_text = "<b>Материалы</b>\n"
#     for material in lesson['files']:
#         file_url = f"<a href='{STATIC_URL}{material['file_path']}'>{material['file_path'].split('/')[-1]}</a>"
#
#         # Проверяем, картинка ли это
#         if material['file_path'].endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
#             file = FSInputFile(f'/home/ivan/Projects/tutor_tg/static{material['file_path']}')
#             material_files_image.append(file)
#         else:
#             materials_text += f"{file_url}\n--------\n"
#
#     homeworks = ''
#     for homework in lesson['homeworks']:
#         homeworks += (f"<a href='{STATIC_URL}{homework['file_path']}"
#                       f"'>{homework['file_path'].split('/')[-1]}</a>\n--------\n")
#     homework_text = f'<b>Домашние задания</b>\n{homeworks}'
#
#     completed_homeworks = ''
#     for completed_homework in lesson['completed_homeworks']:
#         completed_homeworks += (f"<a href='{STATIC_URL}{completed_homework['file_path']}"
#                                 f"'>{completed_homework['file_path'].split('/')[-1]}</a>\n--------\n")
#     completed_homeworks_text = f'<b>Выполненные задания</b>\n{completed_homeworks}'
#
#     comments_by_completed_homeworks = ''
#     for comment_by_completed_homework in lesson['comments_by_completed_homeworks']:
#         comments_by_completed_homeworks += (f"<a href='{STATIC_URL}{comment_by_completed_homework['file_path']}'>"
#                                             f"{comment_by_completed_homework['file_path'].split('/')[-1]}</a>\n--------\n")
#     completed_homeworks_text += f'<b>Комментарии учителя</b>\n{comments_by_completed_homeworks}'
#
#     await message.answer(materials_text, parse_mode='HTML')
#     if material_files_image:
#         for file in material_files_image[:-1]:
#             await message.answer_photo(photo=file)
#         await message.answer_photo(photo=material_files_image[-1])
#     await message.answer(homework_text, parse_mode='HTML')
#     await message.answer(completed_homeworks_text, reply_markup=add_solution_kb(lesson_id), parse_mode='HTML')


async def show_lesson_for_teacher_details(message, lesson_id):
    lesson = await get_lesson_request(lesson_id)
    await message.answer("📒", reply_markup=toggle_lesson_is_done_kb(lesson.get('data', {})))

    material_files_image = []
    materials_text = "<b>Материалы</b>\n"
    for material in lesson.get('data', {}).get('files'):
        file_url = f"<a href='{STATIC_URL}{material.get('file_path')}'>{material.get('file_path').split('/')[-1]}</a>"

        # Проверяем, картинка ли это
        if material.get('file_path').endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            file = FSInputFile(f'/home/ivan/Projects/tutor_tg/static{material.get('file_path')}')
            material_files_image.append(file)
        else:
            materials_text += f"{file_url}\n--------\n"

    homeworks = ''
    for homework in lesson.get('data', {}).get('homeworks'):
        homeworks += (f"<a href='{STATIC_URL}{homework.get('file_path')}"
                      f"'>{homework.get('file_path').split('/')[-1]}</a>\n--------\n")
    homework_text = f'<b>Домашние задания</b>\n{homeworks}'

    completed_homeworks = ''
    for completed_homework in lesson.get('data', {}).get('completed_homeworks'):
        completed_homeworks += (
            f"<a href='{STATIC_URL}{completed_homework.get('file_path')}"
            f"'>{completed_homework.get('file_path').split('/')[-1]}</a>\n--------\n"
        )
    completed_homeworks_text = f'<b>Выполненные задания</b>\n{completed_homeworks}'

    comments_to_completed_homeworks = ''
    for comment_to_completed_homework in lesson.get('data', {}).get('comments_to_completed_homeworks'):
        comments_to_completed_homeworks += (
            f"<a href='{STATIC_URL}{comment_to_completed_homework.get('file_path')}'>"
            f"{comment_to_completed_homework.get('file_path').split('/')[-1]}</a>\n--------\n"
        )
    completed_homeworks_text += f'<b>Комментарии учителя</b>\n{comments_to_completed_homeworks}'

    if material_files_image:
        await message.answer(materials_text, parse_mode='HTML')
        for file in material_files_image[:-1]:
            await message.answer_photo(photo=file)
        await message.answer_photo(
            photo=material_files_image[-1], reply_markup=lesson_files_kb(lesson_id, 'files')
        )
    else:
        await message.answer(
            materials_text, reply_markup=lesson_files_kb(lesson_id, 'files'), parse_mode='HTML'
        )
    await message.answer(
        homework_text, reply_markup=lesson_homework_kb(lesson_id, 'homeworks'), parse_mode='HTML'
    )
    await message.answer(
        completed_homeworks_text, reply_markup=add_comment_kb(lesson_id), parse_mode='HTML'
    )
