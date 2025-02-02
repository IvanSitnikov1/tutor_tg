__all__ = [
    'user_router',
    'lesson_router',
]

from .users.add_user_teacher import user_router
from .users.add_user_student import user_router
from .users.get_users import user_router
from .users.delete_user import user_router
from .users.get_students_for_teacher import user_router
from .users.get_student_for_id import user_router

from .lessons.get_lesson_for_id import lesson_router
