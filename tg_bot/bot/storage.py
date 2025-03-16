from bot.api_helpers.students.api_student_requests import get_students_list_ids_request

STUDENTS = set()


async def update_students():
    global STUDENTS
    students = await get_students_list_ids_request()
    STUDENTS.clear()  # ✅ Очищает множество (ссылка остается)
    STUDENTS.update(students['data'])
    print("✅ Список пользователей обновлен:", STUDENTS)
