from pydantic import BaseModel


class SLesson(BaseModel):
    id: int
    name: str
    file_path: str

    class Config:
        from_attributes  = True
