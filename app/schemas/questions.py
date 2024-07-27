from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1)

    class Config:
        from_attributes = True

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=12)
    category_id: int = Field(..., description='ID категории')

class QuestionResponse(BaseModel):
    text: str
    category: CategoryResponse

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True
