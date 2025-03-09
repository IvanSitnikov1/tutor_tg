from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.api_helpers.teachers.api_teacher_requests import create_teacher_request
from bot.contexts import Form
from bot.functions.teachers.teacher_funcs import show_teacher_menu
from bot.routers import auth_router


@auth_router.callback_query(F.data == 'set_teacher', Form.user_type)
async def set_teacher(call: CallbackQuery, state: FSMContext):
    await state.update_data(user_type='teachers')
    state_data = await state.get_data()
    new_user = await create_teacher_request(state_data.get('username'), call.from_user.id)
    await call.message.answer(new_user.get('detail'))
    if new_user.get('data'):
        await show_teacher_menu(call.message)
    await state.clear()


@auth_router.callback_query(F.data == 'set_student', Form.user_type)
async def set_student(call: CallbackQuery, state: FSMContext):
    await state.update_data(user_type='students')
    await call.message.answer('Введите код, полученный от вашего учителя:')
    await state.set_state(Form.teacher_id)
