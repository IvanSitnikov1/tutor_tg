__all__ = [
    'user_router',
    'lesson_router',
]

from .users.add_user_teacher import user_router
from .users.add_user_student import user_router
from .users.get_users import user_router
from .users.delete_user import user_router
from .users.get_teacher_for_tg_id import user_router
from .users.get_student_for_id import user_router
from .users.add_personal_file import user_router

from .lessons.get_lesson_for_id import lesson_router
from .lessons.add_lesson import lesson_router
from .lessons.add_file_in_lesson import lesson_router
from .lessons.add_homework import lesson_router
from .lessons.delete_lesson import lesson_router
