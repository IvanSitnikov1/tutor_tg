__all__ = [
    'auth_router',
    'teacher_router',
    'student_router',
]

from .auth.auth_handlers import auth_router
from .auth.auth_callbacks import auth_router

from .teachers.teacher_handlers import teacher_router
from .teachers.teacher_callbacks import teacher_router

from .students.student_handlers import student_router
from .students.student_callbacks import student_router
