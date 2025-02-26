from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request, get_lesson_request
from bot.contexts import UploadFile
from bot.keyboards.inline_keyboards import personal_files_kb, lesson_files_kb, add_lesson_homework_kb, \
    toggle_lesson_is_done_kb
from bot.keyboards.reply_reyboards import teacher_menu_kb, student_menu_kb
from config import STATIC_URL


async def show_teacher_menu(message: Message):
    """Отображает меню учителя."""
    await message.answer("Меню", reply_markup=teacher_menu_kb())


async def show_student_menu(message: Message):
    """Отображает меню студента."""
    await message.answer("Меню", reply_markup=student_menu_kb())


async def preparing_for_upload_file(call: CallbackQuery, state: FSMContext, file_type: str):
    lesson_id = call.data.split(':')[1]
    author = await get_teacher_request(call.from_user.id)

    await state.clear()
    await state.update_data(file_type=file_type, lesson_id=lesson_id, author_id=author['id'])
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)


async def show_personal_files(message: Message):
    current_user = await get_teacher_request(message.from_user.id)
    files_text = ''
    for file in current_user['personal_files']:
        files_text += f'{STATIC_URL}{file['file_path']}\n---------\n'
    await message.answer(files_text, reply_markup=personal_files_kb(current_user['id']))


async def show_lesson_details(message, lesson_id):
    lesson = await get_lesson_request(lesson_id)
    await message.answer(".", reply_markup=toggle_lesson_is_done_kb(lesson))

    materials = ''
    for material in lesson['files']:
        materials += f'{STATIC_URL}{material['file_path']}\n--------\n'
    materials_text = f'Материалы\n{materials}'

    homeworks = ''
    for homework in lesson['homeworks']:
        homeworks += f'{STATIC_URL}{homework['file_path']}\n--------\n'
    homework_text = f'Домашние задания\n{homeworks}'

    assignments_text = 'Задания на проверку\n...'
    await message.answer(materials_text, reply_markup=lesson_files_kb(lesson_id))
    await message.answer(homework_text, reply_markup=add_lesson_homework_kb(lesson_id))
    await message.answer(assignments_text)
