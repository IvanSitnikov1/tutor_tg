from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.api_helpers.auth.api_auth_requests import create_user_request
from bot.contexts import Form
from bot.functions import show_teacher_menu
from bot.routers import auth_router


@auth_router.callback_query(F.data == 'set_teacher', Form.user_type)
async def set_teacher(call: CallbackQuery, state: FSMContext):
    await state.update_data(user_type='teacher')
    data = await state.get_data()
    new_user = await create_user_request(data['user_type'], data['username'], call.from_user.id)
    if new_user:
        await call.message.answer('Профиль создан успешно!')
        await call.message.answer(f'Тебя зовут {data['username']}. Твой тип - {data['user_type']}')
        await show_teacher_menu(call.message)
    else:
        await call.message.answer('Не удалось создать профиль')
    await state.clear()


@auth_router.callback_query(F.data == 'set_student', Form.user_type)
async def set_student(call: CallbackQuery, state: FSMContext):
    await state.update_data(user_type='student')
    await call.message.answer('Введите id вашего учителя:')
    await state.set_state(Form.teacher_id)
