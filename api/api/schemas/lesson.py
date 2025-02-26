from pydantic import BaseModel, ConfigDict


class SLessonAdd(BaseModel):
    name: str
    student_id: int


class SLesson(SLessonAdd):
    id: int
    is_done: bool
    files: list['SFile']
    homeworks: list['SFile']

    model_config = ConfigDict(from_attributes=True)


class SFileAdd(BaseModel):
    author_id: int
    lesson_id: int
    file_path: str


class SFile(SFileAdd):
    id: int

    class Config:
        from_attributes = True


class SDeleteFiles(BaseModel):
    files_ids: list[int]
