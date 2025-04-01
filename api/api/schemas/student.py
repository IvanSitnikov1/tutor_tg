from pydantic import BaseModel, Field


class SStudentAdd(BaseModel):
    """Модель для добавления ученика"""

    username: str = Field(description='Имя ученика', examples=['Ivan'])
    id: int = Field(description='tg id ученика', examples=[1234567890])
    teacher_id: int = Field(description='tg id учителя', examples=[1234567890])
