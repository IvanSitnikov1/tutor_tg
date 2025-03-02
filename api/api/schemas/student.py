from pydantic import BaseModel


class SStudentAdd(BaseModel):
    username: str
    id: int
    teacher_id: int
