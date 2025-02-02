from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    username = State()
    user_type = State()
    teacher_id = State()
