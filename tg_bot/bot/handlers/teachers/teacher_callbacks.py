from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.api_helpers.lessons.api_lesson_requests import toggle_lesson_is_done_request, \
    get_lesson_request, delete_lesson_request, delete_files_in_lesson_request, \
    delete_homeworks_in_lesson_request, delete_all_files_requests
from bot.api_helpers.students.api_student_requests import get_student_request, \
    delete_student_request
from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request, delete_personal_files_request
from bot.contexts import AddLesson, UploadFile
from bot.functions.lessons.lesson_funcs import show_lesson_for_teacher_details, pre_upload_file
from bot.functions.teachers.teacher_funcs import show_personal_files
from bot.keyboards.teacher_keyboards import delete_personal_files_by_ids_kb, lessons_of_student_kb, \
    toggle_lesson_is_done_kb, delete_files_kb, students_kb
from bot.routers import teacher_router
from bot.storage import STUDENTS


@teacher_router.callback_query(lambda c: c.data.startswith('show_lessons_of_student:'))
async def show_lessons_of_student(call: CallbackQuery):
    student_id = int(call.data.split(':')[1])
    student = await get_student_request(student_id)
    await call.message.answer(
        f'{student.get('data', {}).get('username')}:',
        reply_markup=lessons_of_student_kb(student.get('data', {})),
    )


@teacher_router.callback_query(
    lambda c: c.data.startswith('show_lesson:') and c.from_user.id not in STUDENTS,
)
async def show_lesson(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    await show_lesson_for_teacher_details(call.message, lesson_id)


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson:'))
async def add_lesson(call: CallbackQuery, state: FSMContext):
    student_id = call.data.split(':')[1]
    await state.clear()
    await state.update_data(student_id=int(student_id))

    await call.message.answer("Введите название урока:")
    await state.set_state(AddLesson.lesson_name)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_lesson:'))
async def delete_lesson(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    response = await delete_lesson_request(lesson_id)

    await call.answer(response.get('detail'), show_alert=True)  # Показываем всплывающее сообщение

    # Получаем ID студента из кнопки "Добавить урок" (чтобы обновить список)
    student_id = int(call.message.reply_markup.inline_keyboard[-1][0].callback_data.split(':')[1])
    student = await get_student_request(student_id)

    # Редактируем текущее сообщение, обновляя список уроков
    await call.message.edit_text(
        text=f'{student.get('username')}:',
        reply_markup=lessons_of_student_kb(student.get('data', {}))
    )


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_file:'))
async def add_lesson_file(call: CallbackQuery, state: FSMContext):
    await pre_upload_file(call, state, "files")


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_homework:'))
async def add_lesson_homework(call: CallbackQuery, state: FSMContext):
    await pre_upload_file(call, state, "homeworks")


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_comment:'))
async def add_lesson_comment(call: CallbackQuery, state: FSMContext):
    await pre_upload_file(call, state, "comments")


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
    await call.message.edit_reply_markup(reply_markup=toggle_lesson_is_done_kb(lesson.get('data')))
    await call.answer("Статус урока изменен", show_alert=True)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_lesson_files:'))
async def delete_lesson_files(call: CallbackQuery, state: FSMContext):
    lesson_id = call.data.split(':')[1]
    file_type = call.data.split(':')[2]
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
    file_id = call.data.split(':')[1]
    lesson_id = call.data.split(':')[2]
    file_type = call.data.split(':')[3]

    lesson = await get_lesson_request(lesson_id)
    current_state = await state.get_data()
    selected_files = current_state.get('selected_files', {})
    selected_files[file_id] = not selected_files.get(file_id, False)
    await state.update_data(selected_files=selected_files)
    await call.message.edit_reply_markup(reply_markup=delete_files_kb(
        lesson.get('data', {}), selected_files, file_type
    ))
    await call.answer()


@teacher_router.callback_query(lambda c: c.data.startswith('delete_selected_files:'))
async def delete_selected_files(call: CallbackQuery, state: FSMContext):
    lesson_id = call.data.split(':')[1]
    file_type = call.data.split(':')[2]

    current_state = await state.get_data()
    selected_files = current_state.get('selected_files', {})

    files_to_delete = [file_id for file_id, is_selected in selected_files.items() if is_selected]
    if files_to_delete:
        if file_type == 'files':
            response = await delete_files_in_lesson_request(files_to_delete)
        else:
            response = await delete_homeworks_in_lesson_request(files_to_delete)

        await call.answer(response.get('detail'), show_alert=True)
        await state.clear()
    else:
        await call.answer("Нет выбранных записей", show_alert=True)

    lesson = await get_lesson_request(lesson_id)
    await call.message.edit_reply_markup(reply_markup=delete_files_kb(
        lesson.get('data', {}), {}, file_type
    ))


@teacher_router.callback_query(lambda c: c.data == 'pre_delete_personal_files')
async def pre_delete_personal_files(call: CallbackQuery, state: FSMContext):
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
    file_id = call.data.split(':')[1]
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
    current_state = await state.get_data()
    selected_files = current_state['selected_files']
    files_to_delete = [file_id for file_id, selected in selected_files.items() if selected]
    if files_to_delete:
        response = await delete_personal_files_request(files_to_delete)
        await call.answer(response.get('detail'), show_alert=True)
    else:
        await call.answer("Нет выбранных записей", show_alert=True)

    user = await get_teacher_request(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=delete_personal_files_by_ids_kb(
        user.get('data'), {}
    ))


@teacher_router.callback_query(lambda c: c.data.startswith('delete_all_lesson_files:'))
async def delete_all_lesson_files(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    file_type = call.data.split(':')[2]

    response = await delete_all_files_requests(lesson_id, file_type)
    await call.message.answer(response.get('detail'))
    await show_lesson_for_teacher_details(call.message, lesson_id)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_all_personal_files:'))
async def delete_all_personal_files(call: CallbackQuery):
    user_id = call.data.split(':')[1]

    user = await get_teacher_request(user_id)
    personal_files_ids = [file.get('id') for file in user.get('data', {}).get('personal_files')]
    response = await delete_personal_files_request(personal_files_ids)
    await call.message.answer(response.get('detail'))
    await show_personal_files(call.message)


@teacher_router.callback_query(lambda c: c.data.startswith('delete_student:'))
async def delete_student(call: CallbackQuery):
    student_id = call.data.split(':')[1]

    deleted_student = await delete_student_request(student_id)
    await call.message.answer(deleted_student.get('detail'))

    current_user = await get_teacher_request(call.message.from_user.id)
    await call.message.edit_text(
        'Ваши студенты:',
        reply_markup=students_kb(current_user.get('data', {}).get('students', [])),
    )
