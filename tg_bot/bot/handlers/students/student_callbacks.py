from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.functions.lessons.lesson_funcs import show_lesson_for_student_details, pre_upload_file
from bot.routers import student_router
from bot.storage import STUDENTS


@student_router.callback_query(
    lambda c: c.data.startswith('show_lesson:') and c.from_user.id in STUDENTS,
)
async def show_lesson(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    await show_lesson_for_student_details(call.message, lesson_id)


@student_router.callback_query(lambda c: c.data.startswith('add_solution:'))
async def add_solution(call: CallbackQuery, state: FSMContext):
    await pre_upload_file(call, state, "solutions")
