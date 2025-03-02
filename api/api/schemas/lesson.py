from pydantic import BaseModel


class SLessonAdd(BaseModel):
    name: str
    student_id: int
    author_id: int


class SFileAdd(BaseModel):
    lesson_id: int
    file_path: str


class SDeleteFiles(BaseModel):
    files_ids: list[int]
