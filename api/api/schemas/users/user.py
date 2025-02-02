from pydantic import BaseModel


class UserAdd(BaseModel):
    username: str
    tg_id: int


class UserTeacherAdd(UserAdd):
    pass


class UserStudentAdd(UserAdd):
    teacher_id: int
