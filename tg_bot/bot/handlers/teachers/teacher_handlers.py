from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.api_helpers.lessons.api_lesson_requests import add_lesson_request
from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request
from bot.contexts import UploadFile, AddLesson
from bot.functions.lessons.lesson_funcs import upload_file_on_server, save_file_in_db, \
    show_lesson_for_teacher_details
from bot.functions.teachers.teacher_funcs import show_teacher_menu, show_personal_files
from bot.keyboards.teacher_keyboards import students_kb
from bot.routers import teacher_router
from bot.storage import STUDENTS


@teacher_router.message(F.text, AddLesson.lesson_name)
async def handle_lesson_name_message(message: Message, state: FSMContext):
    await state.update_data(lesson_name=message.text)
    lesson_data = await state.get_data()
    new_lesson = await add_lesson_request(
        message.from_user.id,
        lesson_data.get('student_id'),
        lesson_data.get('lesson_name'),
    )
    await message.answer(new_lesson.get('detail'))
    await state.clear()
    await show_lesson_for_teacher_details(message, new_lesson.get('data', {}).get('id'))


@teacher_router.message(F.text)
async def handle_teacher_message(message: Message, state: FSMContext):
    if message.text == 'Меню':
        await show_teacher_menu(message)
    elif message.text == '👤Ученики':
        current_user = await get_teacher_request(message.from_user.id)
        await message.answer(
            'Ваши студенты:',
            reply_markup=students_kb(current_user.get('data', {}).get('students', []))
        )
    elif message.text == '📝Личные файлы':
        await show_personal_files(message)


@teacher_router.message(
    lambda message: message.document or message.photo and message.from_user.id not in STUDENTS,
    UploadFile.file,
)
async def handle_upload_file(message: Message, state: FSMContext):
    await upload_file_on_server(message, state)
    saved_file = await save_file_in_db(state)

    await message.answer(f'{saved_file.get('detail')}')
    state_data = await state.get_data()
    # if state_data.get('file_type') in ['solutions', 'comments']:
    #     await show_lesson_by_student_details(message, state_data.get('lesson_id'))
    if state_data.get('file_type') in ['files', 'homeworks', 'comments']:
        await show_lesson_for_teacher_details(message, state_data.get('lesson_id'))
    elif state_data.get('file_type') == 'personal':
        await show_personal_files(message)

    await state.clear()
