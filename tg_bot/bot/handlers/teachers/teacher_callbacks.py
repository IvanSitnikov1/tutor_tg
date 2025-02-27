from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.api_helpers.teachers.api_teacher_requests import get_student_request, delete_lesson_request, \
    toggle_lesson_is_done_request, get_lesson_request, delete_files_in_lesson_request, \
    delete_homeworks_in_lesson_request, get_teacher_request, delete_personal_files_request
from bot.contexts import AddLesson, UploadFile
from bot.functions import preparing_for_upload_file, show_lesson_details
from bot.keyboards.inline_keyboards import student_detail_kb, toggle_lesson_is_done_kb, delete_files_kb, \
    delete_personal_files_kb
from bot.routers import teacher_router


@teacher_router.callback_query(lambda c: c.data.startswith('show_student:'))
async def show_student(call: CallbackQuery):
    student_id = int(call.data.split(':')[1])
    student = await get_student_request(student_id)
    await call.message.answer(f'{student['username']}:', reply_markup=student_detail_kb(student))


@teacher_router.callback_query(lambda c: c.data.startswith('show_lesson:'))
async def show_lesson(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    await show_lesson_details(call.message, lesson_id)


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson:'))
async def add_lesson(call: CallbackQuery, state: FSMContext):
    student_id = call.data.split(':')[1]
    await state.clear()
    await state.update_data(student_id=student_id)

    await call.message.answer("Введите название урока:")
    await state.set_state(AddLesson.lesson_name)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_lesson:'))
async def delete_lesson(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]

    if await delete_lesson_request(lesson_id):
        await call.answer("Урок удален успешно", show_alert=True)  # Показываем всплывающее сообщение

        # Получаем ID студента из кнопки "Добавить урок" (чтобы обновить список)
        student_id = int(call.message.reply_markup.inline_keyboard[-1][0].callback_data.split(':')[1])
        student = await get_student_request(student_id)
        lessons = student['lessons']

        # Редактируем текущее сообщение, обновляя список уроков
        await call.message.edit_text(
            text=f'{student["username"]}:',
            reply_markup=student_detail_kb(lessons)
        )
    else:
        await call.message.answer('Не удаловь удалить урок')


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_file:'))
async def add_lesson_file(call: CallbackQuery, state: FSMContext):
    await preparing_for_upload_file(call, state, "files")


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_homework:'))
async def add_lesson_homework(call: CallbackQuery, state: FSMContext):
    await preparing_for_upload_file(call, state, "homeworks")


@teacher_router.callback_query(lambda c: c.data.startswith('add_personal_file:'))
async def add_personal_file(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(':')[1]
    await state.clear()
    await state.update_data(author_id=user_id)
    await state.update_data(file_type='personal')
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)


@teacher_router.callback_query(lambda c: c.data.startswith('toggle_lesson_is_done:'))
async def toggle_lesson_is_done(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    await toggle_lesson_is_done_request(lesson_id)
    lesson = await get_lesson_request(lesson_id)

    # Обновляем существующее сообщение с кнопкой
    await call.message.edit_reply_markup(reply_markup=toggle_lesson_is_done_kb(lesson))
    await call.answer("Статус урока изменен", show_alert=True)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_lesson_files:'))
async def delete_lesson_files(call: CallbackQuery, state: FSMContext):
    lesson_id = call.data.split(':')[1]
    file_type = call.data.split(':')[2]
    lesson = await get_lesson_request(lesson_id)
    await state.update_data(selected_files={"1": False})
    current_state = await state.get_data()
    await call.message.answer(
        text='Выберите материалы для удаления',
        reply_markup=delete_files_kb(lesson, current_state['selected_files'], file_type)
    )


@teacher_router.callback_query(lambda c: c.data.startswith('toggle_file:'))
async def toggle_file(call: CallbackQuery, state: FSMContext):
    file_id = call.data.split(':')[1]
    lesson_id = call.data.split(':')[2]
    file_type = call.data.split(':')[3]
    current_state = await state.get_data()
    selected_files = current_state['selected_files']
    selected_files[file_id] = not selected_files.get(file_id, False)
    await state.update_data(selected_files=selected_files)
    lesson = await get_lesson_request(lesson_id)
    await call.message.edit_reply_markup(reply_markup=delete_files_kb(lesson, selected_files, file_type))
    await call.answer()


@teacher_router.callback_query(lambda c: c.data.startswith('delete_selected_files:'))
async def delete_selected_files(call: CallbackQuery, state: FSMContext):
    lesson_id = call.data.split(':')[1]
    file_type = call.data.split(':')[2]
    current_state = await state.get_data()
    selected_files = current_state['selected_files']
    files_to_delete = [file_id for file_id, selected in selected_files.items() if selected]
    if files_to_delete:
        if file_type == 'files':
            await delete_files_in_lesson_request(files_to_delete)
        elif file_type == 'homeworks':
            await delete_homeworks_in_lesson_request(files_to_delete)

        await call.answer("Выбранные материалы удалены", show_alert=True)
        await state.update_data(selected_files={"1": False})
    else:
        await call.answer("Нет выбранных записей", show_alert=True)

    lesson = await get_lesson_request(lesson_id)
    await call.message.edit_reply_markup(reply_markup=delete_files_kb(lesson, selected_files, file_type))


@teacher_router.callback_query(lambda c: c.data == 'delete_personal_files')
async def delete_personal_files(call: CallbackQuery, state: FSMContext):
    user = await get_teacher_request(call.from_user.id)
    await state.update_data(selected_files={"1": False})
    current_state = await state.get_data()
    await call.message.answer(
        text='Выберите материалы для удаления',
        reply_markup=delete_personal_files_kb(user, current_state['selected_files'])
    )


@teacher_router.callback_query(lambda c: c.data.startswith('toggle_personal_file:'))
async def toggle_personal_file(call: CallbackQuery, state: FSMContext):
    file_id = call.data.split(':')[1]
    current_state = await state.get_data()
    selected_files = current_state['selected_files']
    selected_files[file_id] = not selected_files.get(file_id, False)
    await state.update_data(selected_files=selected_files)
    user = await get_teacher_request(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=delete_personal_files_kb(user, selected_files))
    await call.answer()


@teacher_router.callback_query(lambda c: c.data == 'delete_selected_personal_files')
async def delete_selected_personal_files(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_data()
    selected_files = current_state['selected_files']
    files_to_delete = [file_id for file_id, selected in selected_files.items() if selected]
    if files_to_delete:
        await delete_personal_files_request(files_to_delete)
        await call.answer("Выбранные материалы удалены", show_alert=True)
        await state.update_data(selected_files={"1": False})
    else:
        await call.answer("Нет выбранных записей", show_alert=True)

    user = await get_teacher_request(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=delete_personal_files_kb(user, selected_files))
