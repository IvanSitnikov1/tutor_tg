from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from bot.api_helpers.lessons.api_lesson_requests import add_lesson_request, \
    update_lesson_date_requests
from bot.api_helpers.teachers.api_teacher_requests import get_teacher_request
from bot.contexts import UploadFile, AddLesson, EditLessonDate
from bot.functions.lessons.lesson_funcs import upload_file_on_server, save_file_in_db, \
    show_lesson_for_teacher_details
from bot.functions.students.student_funcs import show_student_menu
from bot.functions.teachers.teacher_funcs import show_teacher_menu, show_personal_files
from bot.keyboards.teacher_keyboards import students_kb
from bot.routers import teacher_router
from bot.storage import STUDENTS


@teacher_router.message(Command('menu'))
async def cmd_menu(message: Message):
    if message.from_user.id in STUDENTS:
        await show_student_menu(message)
    else:
        await show_teacher_menu(message)


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


@teacher_router.message(F.text.in_({'👤Ученики', '📩 Пригласить ученика', '📝Личные файлы'}))
async def handle_teacher_message(message: Message):
    if message.text == '👤Ученики':
        current_user = await get_teacher_request(message.from_user.id)
        await message.answer(
            'Ваши студенты:',
            reply_markup=students_kb(current_user.get('data', {}).get('students', []))
        )
    elif message.text == '📩 Пригласить ученика':
        await message.answer('Для приглашения нового ученика - сообщите ему свой пригласительный код:')
        await message.answer(f'<code>{message.from_user.id}</code>', parse_mode='HTML')
    elif message.text == '📝Личные файлы':
        await show_personal_files(message)


@teacher_router.message(
    lambda message: (message.document or message.photo or message.video or message.audio)
                    and message.from_user.id not in STUDENTS,
    UploadFile.file,
)
async def handle_upload_file(message: Message, state: FSMContext):
    await upload_file_on_server(message, state)
    saved_file = await save_file_in_db(state)

    await message.answer(f"{saved_file.get('detail')}")
    state_data = await state.get_data()
    if state_data.get('file_type') in ['files', 'homeworks', 'comments']:
        await show_lesson_for_teacher_details(message, state_data.get('lesson_id'))
    elif state_data.get('file_type') == 'personal':
        await show_personal_files(message)

    await state.clear()


@teacher_router.message(F.text, EditLessonDate.new_date)
async def edit_lesson_date(message: Message, state: FSMContext):
    state = await state.get_data()
    lesson_id = int(state.get('lesson_id'))
    new_date = message.text
    response = await update_lesson_date_requests(lesson_id, new_date)
    await message.answer(response.get('detail'))
