from api.configs.app import app
from api.routers.main_router import main_router
from api.handlers import user_router, lesson_router


main_router.include_router(user_router)
main_router.include_router(lesson_router)

app.include_router(main_router)
