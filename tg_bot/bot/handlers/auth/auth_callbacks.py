"""Модуль содержит callback функции для регистрации пользователя"""

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.api_helpers.teachers.api_teacher_requests import create_teacher_request
from bot.contexts import Form
from bot.functions.teachers.teacher_funcs import show_teacher_menu
from bot.routers import auth_router
from loggers import logger


@auth_router.callback_query(F.data == 'set_teacher', Form.user_type)
async def set_teacher(call: CallbackQuery, state: FSMContext):
    """
    Функция обрабатывает нажатие на кнопку с типом учителя, берет данные из контекста и создает нового пользователя
    учителя в базе данных. После успешного создания показывает меню учителя
    """

    logger.info('Выбран тип пользователя "Учитель" при регистрации пользователя')
    await state.update_data(user_type='teachers')
    state_data = await state.get_data()
    new_user = await create_teacher_request(state_data.get('username'), call.from_user.id)
    await call.message.answer(new_user.get('detail'))
    if new_user.get('data'):
        logger.info(f'Пользователь {state_data.get('username')} успешно создан')
        await show_teacher_menu(call.message)
    else:
        logger.error(f'Ошибка при создании пользователя {state_data.get('username')}')
        await call.message.answer('Не удалось зарегистрироваться, попробуйте снова:')
    await state.clear()


@auth_router.callback_query(F.data == 'set_student', Form.user_type)
async def set_student(call: CallbackQuery, state: FSMContext):
    """
    Функция обрабатывает нажатие на кнопку с типом ученика, сохраняет в контексте тип пользователя и запрашивает код
    учителя (tg id) для регистрации студента. Переводит в соответствующее состояние
    (auth_router.handle_set_teacher_for_student)
    """

    logger.info('Выбран тип пользователя "Ученик" при регистрации пользователя')
    await state.update_data(user_type='students')
    await call.message.answer('Введите код, полученный от вашего учителя:')
    await state.set_state(Form.teacher_id)
