__all__ = [
    'Base',
    'User',
    'Teacher',
    'Student',
    'Lesson',
    'File',
    'Homework',
    'PersonalFile'
]

from .user import Base, User, Teacher, Student
from .lesson import Base, Lesson
from .file import Base, File, Homework, PersonalFile
