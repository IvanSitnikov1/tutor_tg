async def show_teacher_menu(message: Message):
    """Отображает меню учителя."""
    await message.answer("Меню", reply_markup=teacher_menu_kb())


async def show_personal_files(message: Message):
    current_user = await get_teacher_request(message.from_user.id)

    material_files_image = []
    files_text = '<b>Файлы</b>\n'
    for personal_file in current_user['personal_files']:
        file_url = (f"<a href='{STATIC_URL}{personal_file['file_path']}'>"
                    f"{personal_file['file_path'].split('/')[-1]}</a>")

        # Проверяем, картинка ли это
        if personal_file['file_path'].endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            file = FSInputFile(f'/home/ivan/Projects/tutor_tg/static{personal_file['file_path']}')
            material_files_image.append(file)
        else:
            files_text += f"{file_url}\n--------\n"
    if material_files_image:
        await message.answer(files_text, parse_mode='HTML')
        for file in material_files_image[:-1]:
            await message.answer_photo(photo=file)
        await message.answer_photo(
            photo=material_files_image[-1], reply_markup=personal_files_kb(current_user['id'])
        )
    else:
        await message.answer(
            files_text, reply_markup=personal_files_kb(current_user['id']), parse_mode='HTML'
        )


async def show_lesson_details(message, lesson_id):
    lesson = await get_lesson_request(lesson_id)
    await message.answer("📒", reply_markup=toggle_lesson_is_done_kb(lesson))

    material_files_image = []
    materials_text = "<b>Материалы</b>\n"
    for material in lesson['files']:
        file_url = f"<a href='{STATIC_URL}{material['file_path']}'>{material['file_path'].split('/')[-1]}</a>"

        # Проверяем, картинка ли это
        if material['file_path'].endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            file = FSInputFile(f'/home/ivan/Projects/tutor_tg/static{material['file_path']}')
            material_files_image.append(file)
        else:
            materials_text += f"{file_url}\n--------\n"

    homeworks = ''
    for homework in lesson['homeworks']:
        homeworks += (f"<a href='{STATIC_URL}{homework['file_path']}"
                      f"'>{homework['file_path'].split('/')[-1]}</a>\n--------\n")
    homework_text = f'<b>Домашние задания</b>\n{homeworks}'

    completed_homeworks = ''
    for completed_homework in lesson['completed_homeworks']:
        completed_homeworks += (f"<a href='{STATIC_URL}{completed_homework['file_path']}"
                                f"'>{completed_homework['file_path'].split('/')[-1]}</a>\n--------\n")
    completed_homeworks_text = f'<b>Выполненные задания</b>\n{completed_homeworks}'

    comments_by_completed_homeworks = ''
    for comment_by_completed_homework in lesson['comments_by_completed_homeworks']:
        comments_by_completed_homeworks += (f"<a href='{STATIC_URL}{comment_by_completed_homework['file_path']}'>"
                                            f"{comment_by_completed_homework['file_path'].split('/')[-1]}</a>\n--------\n")
    completed_homeworks_text += f'<b>Комментарии учителя</b>\n{comments_by_completed_homeworks}'

    if material_files_image:
        await message.answer(materials_text, parse_mode='HTML')
        for file in material_files_image[:-1]:
            await message.answer_photo(photo=file)
        await message.answer_photo(
            photo=material_files_image[-1], reply_markup=lesson_files_kb(lesson_id, 'files')
        )
    else:
        await message.answer(
            materials_text, reply_markup=lesson_files_kb(lesson_id, 'files'), parse_mode='HTML'
        )
    await message.answer(
        homework_text, reply_markup=lesson_homework_kb(lesson_id, 'homeworks'), parse_mode='HTML'
    )
    await message.answer(completed_homeworks_text, reply_markup=add_comment_kb(lesson_id), parse_mode='HTML')