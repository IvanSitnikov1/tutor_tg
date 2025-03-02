__all__ = [
    'lesson_router',
    'teacher_router',
    'student_router',
]

from .lessons.get_lesson_for_id import lesson_router
from .lessons.add_lesson import lesson_router
from .lessons.add_file import lesson_router
from .lessons.add_homework import lesson_router
from .lessons.delete_lesson import lesson_router
from .lessons.change_lesson_is_done import lesson_router
from .lessons.delete_list_files import lesson_router
from .lessons.delete_list_homeworks import lesson_router
from .lessons.add_completed_homework import lesson_router
from .lessons.add_comment_to_completed_homework import lesson_router

from .teachers.add_user_teacher import teacher_router
from .teachers.add_personal_file import teacher_router
from .teachers.delete_list_personal_files import teacher_router
from .teachers.get_teacher_by_id import teacher_router

from .students.add_user_student import student_router
from .students.get_student_by_id import student_router
from .students.get_students_list_ids import student_router
