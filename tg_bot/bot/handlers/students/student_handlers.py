from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot.api_helpers.students.api_student_requests import get_student_request
from bot.api_helpers.teachers.api_teacher_requests import get_lesson_request
from bot.functions import show_student_menu, preparing_for_upload_file, show_lesson_by_student_details
from bot.keyboards.inline_keyboards import show_lessons_student_kb, add_solution_kb
from bot.routers import student_router
from bot.storage import STUDENTS
from config import STATIC_URL


@student_router.message(F.text, lambda message: message.from_user.id in STUDENTS)
async def handle_student_message(message: Message):
    if message.text == 'Меню':
        await show_student_menu()
    elif message.text == 'Уроки':
        student = await get_student_request(message.from_user.id)
        await message.answer('Уроки', reply_markup=show_lessons_student_kb(student['lessons']))


@student_router.callback_query(lambda c: c.data.startswith('show_lesson_student_detail:'))
async def show_lesson_student_detail(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    await show_lesson_by_student_details(call.message, lesson_id)


@student_router.callback_query(lambda c: c.data.startswith('add_lesson_solution:'))
async def add_lesson_solution(call: CallbackQuery, state: FSMContext):
    await preparing_for_upload_file(call, state, "solutions")
