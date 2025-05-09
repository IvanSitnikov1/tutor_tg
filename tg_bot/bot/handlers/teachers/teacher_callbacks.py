"""Модуль содержит callback функции для учителей"""

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.api_helpers.lessons.api_lesson_requests import toggle_lesson_is_done_request, \
    get_lesson_request, delete_lesson_request, delete_files_in_lesson_request, \
    delete_homeworks_in_lesson_request, delete_all_files_requests, update_lesson_date_requests
from bot.api_helpers.students.api_student_requests import get_student_request, \
    delete_student_request
from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request, delete_personal_files_request
from bot.contexts import AddLesson, UploadFile
from bot.functions.lessons.lesson_funcs import show_lesson_for_teacher_details, pre_upload_file
from bot.functions.teachers.teacher_funcs import show_personal_files
from bot.keyboards.teacher_keyboards import delete_personal_files_by_ids_kb, lessons_of_student_kb, \
    toggle_lesson_is_done_kb, delete_files_kb, students_kb, generate_calendar
from bot.routers import teacher_router
from bot.storage import STUDENTS
from loggers import logger


@teacher_router.callback_query(lambda c: c.data.startswith('show_lessons_of_student:'))
async def show_lessons_of_student(call: CallbackQuery):
    """Функция обрабатывает нажатие на кнопку выбранного студента, показывает его уроки"""

    student_id = int(call.data.split(':')[1])
    logger.info(f'Получен запрос на отображение уроков ученика с id {student_id}')
    student = await get_student_request(student_id)
    await call.message.answer(
        f"{student.get('data', {}).get('username')}:",
        reply_markup=lessons_of_student_kb(student.get('data', {})),
    )


@teacher_router.callback_query(
    lambda c: c.data.startswith('show_lesson:') and c.from_user.id not in STUDENTS,
)
async def show_lesson(call: CallbackQuery):
    """Функциял обрабатывает нажатие на урок, показывает содержание конкретного урока"""

    lesson_id = call.data.split(':')[1]
    logger.info(f'Получен запрос на отображение урока с id {lesson_id}')
    await show_lesson_for_teacher_details(call.message, lesson_id)


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson:'))
async def add_lesson(call: CallbackQuery, state: FSMContext):
    """
    Функция обрабатывает нажатие на кнопку добавления урока. Сохраняет id ученика и переходит в следующее
    состояние (handle_lesson_name_message)
    """

    student_id = call.data.split(':')[1]
    logger.info(f'Получен запрос на добавление урока ученику с id {student_id}')
    await state.clear()
    await state.update_data(student_id=int(student_id))

    await call.message.answer("Введите название урока:")
    await state.set_state(AddLesson.lesson_name)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_lesson:'))
async def delete_lesson(call: CallbackQuery):
    """Функция обрабатывает нажатие на кнопку удаления урока и удаляет урок"""

    lesson_id = call.data.split(':')[1]
    logger.info(f'Получен запрос на удаление урока с id {lesson_id}')
    response = await delete_lesson_request(lesson_id)
    logger.info(response.get('detail'))

    await call.answer(response.get('detail'), show_alert=True)  # Показываем всплывающее сообщение

    # Получаем ID студента из кнопки "Добавить урок" (чтобы обновить список)
    student_id = int(call.message.reply_markup.inline_keyboard[-1][0].callback_data.split(':')[1])
    logger.info(f'Обновляем список уроков ученика с id {student_id} после удаления урока')
    student = await get_student_request(student_id)

    # Редактируем текущее сообщение, обновляя список уроков
    await call.message.edit_text(
        text=f"{student.get('username')}:",
        reply_markup=lessons_of_student_kb(student.get('data', {}))
    )


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_file:'))
async def add_lesson_file(call: CallbackQuery, state: FSMContext):
    """
    Функция обрабатывает нажатие на кнопку добавления файла урока, вызывает функцию
    подготовки к добавлению файла, передавая его тип и контекст
    """

    logger.info('Получен запрос на добавление материала к уроку')
    await pre_upload_file(call, state, "files")


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_homework:'))
async def add_lesson_homework(call: CallbackQuery, state: FSMContext):
    """
    Функция обрабатывает нажатие на кнопку добавления домашнего задания урока, вызывает функцию
    подготовки к добавлению файла, передавая его тип и контекст
    """

    logger.info('Получен запрос на добавление домашнего задания к уроку')
    await pre_upload_file(call, state, "homeworks")


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_comment:'))
async def add_lesson_comment(call: CallbackQuery, state: FSMContext):
    """
    Функция обрабатывает нажатие на кнопку добавления комментария к домашнему заданию урока, вызывает функцию
    подготовки к добавлению файла, передавая его тип и контекст
    """

    logger.info('Получен запрос на добавление комментария к уроку')
    await pre_upload_file(call, state, "comments")


@teacher_router.callback_query(lambda c: c.data.startswith('add_personal_file:'))
async def add_personal_file(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие на кнопку добавления личного файла и переходит в состояние загрузки файла"""

    user_id = call.data.split(':')[1]
    logger.info(f'Получен запрос на добавление личного файла пользователя с id {user_id}')
    await state.clear()
    await state.update_data(author_id=user_id)
    await state.update_data(file_type='personal')
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)


@teacher_router.callback_query(lambda c: c.data.startswith('toggle_lesson_is_done:'))
async def toggle_lesson_is_done(call: CallbackQuery):
    """Функция обрабатывает нажатие на название урока в открытом уроке. Изменяет его статус (выполнен/не выполнен)"""

    lesson_id = call.data.split(':')[1]
    logger.info('Получен запрос на изменение состояния урока')
    await toggle_lesson_is_done_request(lesson_id)
    lesson = await get_lesson_request(lesson_id)

    if lesson.get('data'):
        logger.info('Состояние урока успешно изменено')
        # Обновляем существующее сообщение с кнопкой
        await call.message.edit_reply_markup(reply_markup=toggle_lesson_is_done_kb(lesson.get('data')))
        await call.answer('Статус урока изменен', show_alert=True)
    else:
        logger.error('Не удалось изменить состояние урока')
        await call.answer('Не удалось изменить состояние урока', show_alert=True)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_lesson_files:'))
async def delete_lesson_files(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие на кнопку удаления нескольких файлов урока. Выводит список файлов для удаления"""

    lesson_id = call.data.split(':')[1]
    file_type = call.data.split(':')[2]
    logger.info(f'Получен запрос на начало удаления нескольких файлов типа - {file_type} из урока с id {lesson_id}')
    lesson = await get_lesson_request(lesson_id)
    current_state = await state.get_data()
    await call.message.answer(
        text='Выберите материалы для удаления',
        reply_markup=delete_files_kb(
            lesson.get('data', {}),
            current_state.get('selected_files', {}),
            file_type,
        )
    )


@teacher_router.callback_query(lambda c: c.data.startswith('toggle_file:'))
async def toggle_file(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие на файл урока при удалении, отмечает файл галочкой и добавляет в контекст"""

    file_id = call.data.split(':')[1]
    lesson_id = call.data.split(':')[2]
    file_type = call.data.split(':')[3]
    logger.info(f'Получен запрос на изменение состояния файла с id {file_id}')

    lesson = await get_lesson_request(lesson_id)
    current_state = await state.get_data()
    selected_files = current_state.get('selected_files', {})
    # Добавляем файл в контекст, если его нет или изменяем состояние на противоположное
    selected_files[file_id] = not selected_files.get(file_id, False)
    await state.update_data(selected_files=selected_files)
    await call.message.edit_reply_markup(reply_markup=delete_files_kb(
        lesson.get('data', {}), selected_files, file_type
    ))
    await call.answer()


@teacher_router.callback_query(lambda c: c.data.startswith('delete_selected_files:'))
async def delete_selected_files(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие кнопки удаления выбранных файлов, собирает id файлов из контекста и удаляет"""

    lesson_id = call.data.split(':')[1]
    file_type = call.data.split(':')[2]
    logger.info(f'Получен запрос на подтверждение удаления нескольких файлов типа - {file_type} из урока с id {lesson_id}')

    current_state = await state.get_data()
    selected_files = current_state.get('selected_files', {})

    files_to_delete = [file_id for file_id, is_selected in selected_files.items() if is_selected]
    if files_to_delete:
        if file_type == 'files':
            response = await delete_files_in_lesson_request(files_to_delete)
        else:
            response = await delete_homeworks_in_lesson_request(files_to_delete)

        try:
            logger.error('Не удалось удалить файлы')
            await call.answer(response.get('detail'), show_alert=True)
        except AttributeError:
            logger.info('Файлы успешно удалены')
            await call.answer('Файлы успешно удалены', show_alert=True)
        await state.clear()
    else:
        logger.error('Нет выбранных файлов для удаления')
        await call.answer("Нет выбранных записей", show_alert=True)

    lesson = await get_lesson_request(lesson_id)
    # Обновляем клавиатуру со списком файлов для удаления после удаления
    await call.message.edit_reply_markup(reply_markup=delete_files_kb(
        lesson.get('data', {}), {}, file_type
    ))


@teacher_router.callback_query(lambda c: c.data == 'pre_delete_personal_files')
async def pre_delete_personal_files(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие на кнопку удаления нескольких личных файлов. Выводит список файлов для удаления"""

    logger.info('Получен запрос на начало удаления нескольких личных файлов учителя')
    user = await get_teacher_request(call.from_user.id)
    current_state = await state.get_data()
    await call.message.answer(
        text='Выберите материалы для удаления',
        reply_markup=delete_personal_files_by_ids_kb(
            user.get('data', {}),
            current_state.get('selected_files', {}),
        ),
    )


@teacher_router.callback_query(lambda c: c.data.startswith('toggle_personal_file:'))
async def toggle_personal_file(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие на личный файл при удалении, отмечает файл галочкой и добавляет в контекст"""

    file_id = call.data.split(':')[1]
    logger.info(f'Получен запрос на изменение состояния личного файла с id {file_id}')
    current_state = await state.get_data()
    selected_files = current_state.get('selected_files', {})
    selected_files[file_id] = not selected_files.get(file_id, False)
    await state.update_data(selected_files=selected_files)
    user = await get_teacher_request(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=delete_personal_files_by_ids_kb(
        user.get('data', {}), selected_files))
    await call.answer()


@teacher_router.callback_query(lambda c: c.data == 'delete_selected_personal_files')
async def delete_selected_personal_files(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие кнопки удаления выбранных файлов, собирает id файлов из контекста и удаляет"""

    logger.info('Получен запрос на подтверждение удаления нескольких личных файлов учителя')
    current_state = await state.get_data()
    selected_files = current_state['selected_files']
    files_to_delete = [file_id for file_id, selected in selected_files.items() if selected]
    if files_to_delete:
        response = await delete_personal_files_request(files_to_delete)
        try:
            logger.error('Не удалось удалить файлы')
            await call.answer(response.get('detail'), show_alert=True)
        except AttributeError:
            logger.info('Файлы успешно удалены')
            await call.answer('Файлы успешно удалены', show_alert=True)
        await state.clear()
    else:
        logger.error('Нет выбранных файлов для удаления')
        await call.answer("Нет выбранных записей", show_alert=True)

    user = await get_teacher_request(call.from_user.id)
    # Обновляем клавиатуру со списком файлов для удаления после удаления
    await call.message.edit_reply_markup(reply_markup=delete_personal_files_by_ids_kb(
        user.get('data'), {}
    ))


@teacher_router.callback_query(lambda c: c.data.startswith('delete_all_lesson_files:'))
async def delete_all_lesson_files(call: CallbackQuery):
    """Функция обрабатывает нажатие на кнопку удаления всех файлов урока, удаляет их и показывает обновленный урок"""

    lesson_id = call.data.split(':')[1]
    file_type = call.data.split(':')[2]
    logger.info(f'Получен запрос на удаление всех файлов типа - {file_type} из урока с id {lesson_id}')

    response = await delete_all_files_requests(lesson_id, file_type)
    try:
        logger.error('Не удалось удалить файлы')
        await call.answer(response.get('detail'), show_alert=True)
    except AttributeError:
        logger.info('Файлы успешно удалены')
        await call.answer('Файлы успешно удалены', show_alert=True)
    await show_lesson_for_teacher_details(call.message, lesson_id)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_all_personal_files:'))
async def delete_all_personal_files(call: CallbackQuery):
    """Функция обрабатывает нажатие на кнопку удаления всех личных файлов, удаляет их и показывает обновленные файлы"""

    user_id = call.data.split(':')[1]
    logger.info(f'Получен запрос на удаление всех личных файлов пользователя с id {user_id}')

    user = await get_teacher_request(user_id)
    personal_files_ids = [file.get('id') for file in user.get('data', {}).get('personal_files')]
    response = await delete_personal_files_request(personal_files_ids)
    try:
        logger.error('Не удалось удалить файлы')
        await call.answer(response.get('detail'), show_alert=True)
    except AttributeError:
        logger.info('Файлы успешно удалены')
        await call.answer('Файлы успешно удалены', show_alert=True)
    await show_personal_files(call.message)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_student:'))
async def delete_student(call: CallbackQuery):
    """Функция обрабатывает нажатие на кнопку удаления ученика, удаляет его и обновляет список учеников"""

    student_id = call.data.split(':')[1]
    logger.info(f'Получен запрос на удаление ученика с id {student_id}')

    deleted_student = await delete_student_request(student_id)
    logger.info(deleted_student.get('detail'))
    await call.message.answer(deleted_student.get('detail'))

    current_user = await get_teacher_request(call.message.from_user.id)
    await call.message.edit_text(
        'Ваши студенты:',
        reply_markup=students_kb(current_user.get('data', {}).get('students', [])),
    )


@teacher_router.callback_query(lambda c: c.data.startswith("select_date_"))
async def process_date_selection(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает нажатие кнопки с выбранной датой урока и устанавливает эту дату в урок"""

    # Дата в формате "дд-мм-гггг"
    new_date = call.data.split("_")[2]

    state = await state.get_data()
    lesson_id = int(state.get('lesson_id'))
    logger.info(f'Получен запрос на изменение даты урока с id {lesson_id} на {new_date}')
    response = await update_lesson_date_requests(lesson_id, new_date)
    await call.message.answer(f"✅ Вы выбрали дату: {new_date}")
    logger.info(response.get('detail'))
    await call.message.answer(response.get('detail'))
    await call.answer()


@teacher_router.callback_query(lambda c: c.data.startswith("change_month_"))
async def process_change_month(callback: CallbackQuery):
    """Функция обрабатывает нажатие на кнопку смены месяца в клавиатуре с выбором даты и обновляет эту клавиатуру"""

    logger.info('Получен запрос на смену месяца на клавиатуре с выбором даты урока')
    _, _, year, month = callback.data.split("_")
    year, month = int(year), int(month)

    await callback.message.edit_text(
        "📅 Выбери дату проведения урока:",
        reply_markup=generate_calendar(year, month)
    )
    await callback.answer()
