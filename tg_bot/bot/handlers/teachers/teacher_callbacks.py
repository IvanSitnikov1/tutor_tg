from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.api_helpers.teachers.api_teacher_requests import get_student_request, delete_lesson_request
from bot.contexts import AddLesson, UploadFile
from bot.functions import preparing_for_upload_file, show_lesson_details
from bot.keyboards.inline_keyboards import student_detail_kb
from bot.routers import teacher_router


@teacher_router.callback_query(lambda c: c.data.startswith('show_student:'))
async def show_student(call: CallbackQuery):
    student_id = int(call.data.split(':')[1])
    student = await get_student_request(student_id)
    lessons = student['lessons']
    await call.message.answer(f'{student['username']}:', reply_markup=student_detail_kb(lessons))


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
