from api.configs.app import app
from api.routers.main_router import main_router
from api.handlers import lesson_router, teacher_router, student_router


main_router.include_router(teacher_router)
main_router.include_router(student_router)
main_router.include_router(lesson_router)

app.include_router(main_router)
