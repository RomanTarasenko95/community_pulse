from pydantic import BaseModel, Field


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=12)


class QuestionResponse(BaseModel):
    text: str

    class Config:
        # Указываем Pydantic использовать эти параметры чтобы можно было переносить данные прямо с объекта
        from_attributes = True


class MessageResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True
