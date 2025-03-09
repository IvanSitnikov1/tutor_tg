from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    username = State()
    user_type = State()
    teacher_id = State()


class AddLesson(StatesGroup):
    student_id = State()
    lesson_name = State()


class UploadFile(StatesGroup):
    author_id = State()
    lesson_id = State()
    file = State()
    file_type = State()
    file_name = State()


class SelectedFiles(StatesGroup):
    selected_files = State()
