from pydantic import BaseModel, ConfigDict

from api.schemas.lesson import SLesson


class SUserAdd(BaseModel):
    username: str
    tg_id: int


class STeacherAdd(SUserAdd):
    pass


class SStudentAdd(SUserAdd):
    teacher_id: int


class SStudent(BaseModel):
    id: int
    username: str
    lessons: list[SLesson]

    model_config = ConfigDict(from_attributes=True)


class SPersonalFileAdd(BaseModel):
    author_id: int
    file_path: str
