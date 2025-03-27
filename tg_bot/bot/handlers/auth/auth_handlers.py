from datetime import datetime

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.api_helpers.students.api_student_requests import create_student_request
from bot.functions.students.student_funcs import show_student_menu
from bot.keyboards.auth_keyboards import user_type_kb
from bot.keyboards.teacher_keyboards import generate_calendar
from bot.routers import auth_router
from bot.contexts import Form, EditLessonDate
from bot.storage import update_students


@auth_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    args = message.text.split(' ')
    if len(args) > 1:
        params = args[1]
        parts = params.split('_')
        if params.startswith('edit_date'):
            await state.update_data(lesson_id=parts[2])
            now = datetime.now()
            await message.answer(
                '📅 Выбери дату проведения урока:',
                reply_markup=generate_calendar(now.year, now.month),
            )
    else:
        await state.clear()
        await message.answer('Привет! Как тебя зовут?')
        await state.set_state(Form.username)


@auth_router.message(F.text, Form.username)
async def handle_set_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Выбери свою роль:' , reply_markup=user_type_kb())
    await state.set_state(Form.user_type)


@auth_router.message(F.text, Form.teacher_id)
async def handle_set_teacher_for_student(message: Message, state: FSMContext):
    try:
        await state.update_data(teacher_id=int(message.text))
    except ValueError:
        await message.answer('Введите корректный числовой код:')
        return

    data = await state.get_data()
    new_user = await create_student_request(
        data.get('username'),
        message.from_user.id,
        teacher_id=data.get('teacher_id'),
    )
    await message.answer(new_user.get('detail'))
    if new_user.get('data'):
        await update_students()
        await show_student_menu(message)
    else:
        await message.answer('Не удалось зарегистрироваться, попробуйте снова:')
    await state.clear()
