from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request
from bot.contexts import UploadFile
from bot.functions.lessons.lesson_funcs import upload_file_on_server, save_file_in_db, \
    show_lesson_for_student_details

from bot.api_helpers.students.api_student_requests import get_student_request
from bot.keyboards.student_keyboards import show_lessons_of_student_kb
from bot.routers import student_router
from bot.storage import STUDENTS


@student_router.message(
    F.text.in_({'📒Уроки'}),
    lambda message: message.from_user.id in STUDENTS,
)
async def handle_student_message(message: Message):
    if message.text == '📒Уроки':
        student = await get_student_request(message.from_user.id)
        await message.answer('Уроки', reply_markup=show_lessons_of_student_kb(student.get('data', {}).get('lessons')))


@student_router.message(
    lambda message: (message.document or message.photo or message.video or message.audio)
                    and message.from_user.id in STUDENTS,
    UploadFile.file,
)
async def handle_upload_file(message: Message, state: FSMContext):
    await upload_file_on_server(message, state)
    saved_file = await save_file_in_db(state)

    await message.answer(f'{saved_file.get('detail')}')
    state_data = await state.get_data()
    await show_lesson_for_student_details(message, state_data.get('lesson_id'))

    await state.clear()


@student_router.message()
async def handle_unknown(message: Message):
    student = await get_student_request(message.from_user.id)
    teacher = await get_teacher_request(message.from_user.id)
    if student.get('data', None) or teacher.get('data', None):
        await message.answer("Извините, я не понимаю ваше сообщение. Попробуйте открыть "
                             "меню(/menu).")
    else:
        await message.answer('Для использования бота нужно зарегистрироваться(/start).')
