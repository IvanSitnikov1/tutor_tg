from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.contexts import UploadFile
from bot.functions.lessons.lesson_funcs import upload_file_on_server, save_file_in_db, \
    show_lesson_for_student_details
from bot.functions.students.student_funcs import show_student_menu

from bot.api_helpers.students.api_student_requests import get_student_request
from bot.keyboards.student_keyboards import show_lessons_of_student_kb
from bot.routers import student_router
from bot.storage import STUDENTS


@student_router.message(F.text, lambda message: message.from_user.id in STUDENTS)
async def handle_student_message(message: Message):
    if message.text == 'Меню':
        await show_student_menu(message)
    elif message.text == '📒Уроки':
        student = await get_student_request(message.from_user.id)
        await message.answer('Уроки', reply_markup=show_lessons_of_student_kb(student.get('data', {}).get('lessons')))


@student_router.message(
    lambda message: (message.document or message.photo) and message.from_user.id in STUDENTS,
    UploadFile.file,
)
async def handle_upload_file(message: Message, state: FSMContext):
    await upload_file_on_server(message, state)
    saved_file = await save_file_in_db(state)

    await message.answer(f'{saved_file.get('detail')}')
    state_data = await state.get_data()
    await show_lesson_for_student_details(message, state_data.get('lesson_id'))

    await state.clear()
