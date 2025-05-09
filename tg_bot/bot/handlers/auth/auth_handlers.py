"""Модуль содержит обработчики для процесса регистрации пользователя"""

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
from bot.contexts import Form
from bot.storage import update_students
from loggers import logger


@auth_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """
    Функция обработчика команды /start. Если передана без аргументов  - запрашивает имя пользователя и
    переводит в нужное состояние (handle_set_username). Если с аргументами - обрабатывает изменение даты урока
    """

    logger.info('Запущен обработчик комманды /start')
    args = message.text.split(' ')
    if len(args) > 1:
        params = args[1]
        parts = params.split('_')
        if params.startswith('edit_date'):
            logger.info('Получена команда на установку даты урока')
            await state.update_data(lesson_id=parts[2])
            now = datetime.now()
            # Вызываем клавиатуру с выбором даты, показывающую текущий месяц текущего года
            await message.answer(
                '📅 Выбери дату проведения урока:',
                reply_markup=generate_calendar(now.year, now.month),
            )
    else:
        logger.info('Получен запрос на регистрацию пользователя')
        await state.clear()
        await message.answer('Привет! Как тебя зовут?')
        await state.set_state(Form.username)


@auth_router.message(F.text, Form.username)
async def handle_set_username(message: Message, state: FSMContext):
    """
    Функция сохраняет в контексте имя пользователя, запрашивает его роль и переводит в нужное состояние через
    callback при нажатии соответствующей кнопки клавиатуры (set_teacher или set_student)
    """

    logger.info('Получено и установлено имя нового пользователя')
    await state.update_data(username=message.text)
    await message.answer('Выбери свою роль:' , reply_markup=user_type_kb())
    await state.set_state(Form.user_type)


@auth_router.message(F.text, Form.teacher_id)
async def handle_set_teacher_for_student(message: Message, state: FSMContext):
    """Функция устанавливает учителя для ученика при регистрации и создает соответствующего пользователя в базе данных"""

    logger.info('Получен код учителя при регистрации ученика')
    # Валидируем сообщение и возвращаем в то же состояние при ошибке
    try:
        await state.update_data(teacher_id=int(message.text))
    except ValueError:
        logger.error('Получен невалидный код учителя')
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
        logger.info(f'Ученик {data.get('username')} успешно создан')
        await update_students()
        await show_student_menu(message)
    else:
        logger.error(f'Не удалось создать учениика {data.get('username')}')
        await message.answer('Не удалось зарегистрироваться, попробуйте снова:')
    await state.clear()
