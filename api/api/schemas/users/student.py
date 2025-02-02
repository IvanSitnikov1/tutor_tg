from pydantic import BaseModel

from api.schemas.users.lesson import SLesson


class SStudent(BaseModel):
    id: int
    username: str
    lessons: list[SLesson]

    class Config:
        from_attributes  = True
