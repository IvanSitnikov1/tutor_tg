from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.api_helpers.auth.api_auth_requests import create_user_request
from bot.functions import show_student_menu
from bot.keyboards.inline_keyboards import user_type_kb
from bot.routers import auth_router
from bot.contexts import Form


@auth_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет! Как тебя зовут?')
    await state.set_state(Form.username)


@auth_router.message(F.text, Form.username)
async def handler_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Выбери свою роль:' , reply_markup=user_type_kb())
    await state.set_state(Form.user_type)


@auth_router.message(F.text, Form.teacher_id)
async def handler_set_teacher(message: Message, state: FSMContext):
    await state.update_data(teacher_id=int(message.text))
    data = await state.get_data()
    new_user = await create_user_request(data['user_type'], data['username'], message.from_user.id, teacher_id=data['teacher_id'])
    if new_user:
        await message.answer('Профиль создан успешно!')
        await message.answer(f'Тебя зовут {data['username']}. Твой тип - {data['user_type']}')
        await show_student_menu(message)
    else:
        await message.answer('Не удалось создать профиль')
    await state.clear()
