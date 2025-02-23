from pydantic import BaseModel, ConfigDict

from api.schemas.lesson import SLesson


class SStudent(BaseModel):
    id: int
    username: str
    lessons: list[SLesson]

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes  = True
