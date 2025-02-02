__all__ = [
    'auth_router',
    'teacher_router',
]

from .auth.auth_handlers import auth_router
from .teachers.teacher_handlers import teacher_router
