import os

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot.api_helpers.teachers.api_teacher_requests import get_teacher_with_students_request, get_student_request, \
    get_lesson_request, \
    add_lesson_request, delete_lesson_request, upload_file_in_lesson, upload_homework, upload_personal_file
from bot.contexts import AddLesson, UploadFile
from bot.functions import teacher_menu
from bot.keyboards.inline_keyboards import students_kb, student_detail_kb, add_lesson_file_kb, add_lesson_homework_kb, \
    personal_files_kb
from bot.routers import teacher_router
from config import STATIC_URL


@teacher_router.message(F.text)
async def handler_teacher_message(message: Message, state: FSMContext):
    if message.text == 'Меню':
        await teacher_menu(message)
    elif message.text == 'Ученики':
        current_user = await get_teacher_with_students_request(message.from_user.id)
        await message.answer('Ваши студенты:', reply_markup=students_kb(current_user['students']))
    elif message.text == 'Личные файлы':
        current_user = await get_teacher_with_students_request(message.from_user.id)
        files_text = ''
        for file in current_user['personal_files']:
            files_text += f'{STATIC_URL}{file['file_path']}\n---------\n'
        await message.answer(files_text, reply_markup=personal_files_kb(current_user['id']))
    else:
        await state.update_data(lesson_name=message.text)
        lesson_data = await state.get_data()
        new_lesson = await add_lesson_request(lesson_data['student_id'], lesson_data['lesson_name'])
        if new_lesson:
            await message.answer("Урок добавлен успешно")
            # lesson_id =  new_lesson['id']
            # lesson_text, materials_text, homework_text, assignments_text = await show_lesson_details(lesson_id)
            #
            # await message.answer(lesson_text)
            # await message.answer(materials_text, reply_markup=add_lesson_file_kb(student_id))
            # await message.answer(homework_text, reply_markup=add_lesson_homework_kb())
            # await message.answer(assignments_text)
        else:
            await message.answer("Не получилось добавить урок")
    await state.clear()


@teacher_router.callback_query(lambda c: c.data.startswith('show_student:'))
async def show_student(call: CallbackQuery):
    student_id = int(call.data.split(':')[1])
    student = await get_student_request(student_id)
    lessons = student['lessons']
    await call.message.answer(f'{student['username']}:', reply_markup=student_detail_kb(lessons))


async def show_lesson_details(lesson_id):
    lesson = await get_lesson_request(lesson_id)
    lesson_text = f'Урок {lesson["name"]}:'

    materials = ''
    for material in lesson['files']:
        materials += f'{STATIC_URL}{material['file_path']}\n--------\n'
    materials_text = f'Материалы\n{materials}'

    homeworks = ''
    for homework in lesson['homeworks']:
        homeworks += f'{STATIC_URL}{homework['file_path']}\n--------\n'
    homework_text = f'Домашние задания\n{homeworks}'

    assignments_text = 'Задания на проверку\n...'
    return lesson_text, materials_text, homework_text, assignments_text


@teacher_router.callback_query(lambda c: c.data.startswith('show_lesson:'))
async def show_lesson(call: CallbackQuery):
    lesson_id = call.data.split(':')[1]
    lesson_text, materials_text, homework_text, assignments_text = await show_lesson_details(lesson_id)

    await call.message.answer(lesson_text)
    await call.message.answer(materials_text, reply_markup=add_lesson_file_kb(lesson_id))
    await call.message.answer(homework_text, reply_markup=add_lesson_homework_kb(lesson_id))
    await call.message.answer(assignments_text)


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
    lesson_id = call.data.split(':')[1]
    author = await get_teacher_with_students_request(call.from_user.id)

    await state.clear()
    await state.update_data(file_type='files')
    await state.update_data(lesson_id=lesson_id)
    await state.update_data(author_id=author['id'])
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)


@teacher_router.callback_query(lambda c: c.data.startswith('add_lesson_homework:'))
async def add_lesson_homework(call: CallbackQuery, state: FSMContext):
    lesson_id = call.data.split(':')[1]
    author = await get_teacher_with_students_request(call.from_user.id)

    await state.clear()
    await state.update_data(file_type='homeworks')
    await state.update_data(lesson_id=lesson_id)
    await state.update_data(author_id=author['id'])
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)


@teacher_router.message(lambda message: message.document or message.photo, UploadFile.file)
async def handle_upload_file(message: Message, state: FSMContext):
    file = None
    file_name = None
    if message.document:
        file = message.document
        file_name = file.file_name
    if message.photo:
        file = message.photo[-1]
        file_name = f'{file.file_id}.jpg'

    state_data = await state.get_data()
    file_path = os.path.join(f'/home/ivan/Projects/tutor_tg/static/{state_data['file_type']}', file_name)

    file_info = await message.bot.get_file(file.file_id)
    await message.bot.download_file(file_info.file_path, file_path)

    if state_data['file_type'] == 'files':
        link_file = await upload_file_in_lesson(state_data['author_id'], state_data['lesson_id'], file_name)
    elif state_data['file_type'] == 'homeworks':
        link_file = await upload_homework(state_data['author_id'], state_data['lesson_id'], file_name)
    else:
        link_file = await upload_personal_file(state_data['author_id'], file_name)

    if link_file:
        await message.answer('Файл успешно загружен')
        if state_data.get('lesson_id'):
            lesson_text, materials_text, homework_text, assignments_text = await show_lesson_details(state_data['lesson_id'])

            await message.answer(lesson_text)
            await message.answer(materials_text, reply_markup=add_lesson_file_kb(state_data['lesson_id']))
            await message.answer(homework_text, reply_markup=add_lesson_homework_kb(state_data['lesson_id']))
            await message.answer(assignments_text)
            # doc_file = FSInputFile(file_path)
            # await message.answer_document(document=doc_file)
        else:
            current_user = await get_teacher_with_students_request(message.from_user.id)
            files_text = ''
            for file in current_user['personal_files']:
                files_text += f'{STATIC_URL}{file['file_path']}\n---------\n'
            await message.answer(files_text, reply_markup=personal_files_kb(current_user['id']))
    else:
        await message.answer("❌ Файл не найден.")
    await state.clear()


@teacher_router.callback_query(lambda c: c.data.startswith('add_personal_file:'))
async def add_personal_file(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(':')[1]
    await state.clear()
    await state.update_data(author_id=user_id)
    await state.update_data(file_type='personal')
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)
