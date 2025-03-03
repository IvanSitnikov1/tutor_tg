async def preparing_for_upload_file(call: CallbackQuery, state: FSMContext, file_type: str):
    lesson_id = call.data.split(':')[1]
    if file_type in ['files', 'homeworks', 'comments']:
        author = await get_teacher_request(call.from_user.id)
    else:
        author = await get_student_request(call.from_user.id)

    await state.clear()
    await state.update_data(file_type=file_type, lesson_id=lesson_id, author_id=author['id'])
    await call.message.answer("📄 Пожалуйста, загрузите файл.")
    await state.set_state(UploadFile.file)