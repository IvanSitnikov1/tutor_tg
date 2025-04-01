from pydantic import BaseModel, Field


class STeacherAdd(BaseModel):
    """Модель для добавления учителя"""

    username: str = Field(description='Имя учителя', examples=['Ivan'])
    id: int = Field(description='tg id учителя', examples=[1234567890])

class SPersonalFileAdd(BaseModel):
    """Модель для добавления личного файла учителя"""

    author_id: int = Field(description='tg id учителя', examples=[1234567890])
    file_path: str = Field(description='Путь к личному файлу', examples=['personal_files/file_name.pdf'])
