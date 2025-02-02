from aiogram import F
from aiogram.types import Message, CallbackQuery

from bot.api_helpers.teachers.api_teacher_requests import get_students_request, get_student_request, get_lesson_request
from bot.keyboards.inline_keyboards import students_kb, student_detail_kb, add_homework_kb, add_lesson_kb
from bot.routers import teacher_router


@teacher_router.message(F.text)
async def handler_teacher_message(message: Message):
    if message.text == 'Ученики':
        students = await get_students_request(message.from_user.id)
        await message.answer('Ваши студенты:', reply_markup=students_kb(students))
        # await teacher_menu(message)


@teacher_router.callback_query(lambda c: c.data.startswith('show_student:'))
async def show_student(call: CallbackQuery):
    student_id = int(call.data.split(':')[1])
    student = await get_student_request(student_id)
    lessons = student['lessons']
    await call.message.answer(f'{student['username']}:', reply_markup=student_detail_kb(lessons))


@teacher_router.callback_query(lambda c: c.data.startswith('show_lesson:'))
async def show_lesson(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    lesson = await get_lesson_request(lesson_id)
    await call.message.answer(f'Урок {lesson['name']}:')
    await call.message.answer('Материалы\n...', reply_markup=add_lesson_kb())
    await call.message.answer('Домашние задания\n...', reply_markup=add_homework_kb())
    await call.message.answer('Задания на проверку\n...')
