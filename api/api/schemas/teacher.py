from pydantic import BaseModel


class STeacherAdd(BaseModel):
    username: str
    id: int

class SPersonalFileAdd(BaseModel):
    author_id: int
    file_path: str
