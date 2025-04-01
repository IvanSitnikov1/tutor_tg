from pydantic import BaseModel, Field


class SLessonAdd(BaseModel):
    """Модель для добавления урока"""

    name: str = Field(description='Название урока', examples=['lesson 1'])
    student_id: int = Field(description='tg id ученика', examples=[1234567890])
    author_id: int = Field(description='tg id учителя', examples=[1234567890])


class SFileAdd(BaseModel):
    """Модель для добавления файла к уроку"""

    lesson_id: int = Field(description='id урока', examples=[1])
    file_path: str = Field(description='Путь к файлу урока', examples=['/files/file_name.pdf'])


class SDeleteFiles(BaseModel):
    """Модель для удаления списка файлов урока"""

    files_ids: list[int] = Field(description='Список id файлов урока', examples=[[1, 2, 3]])
