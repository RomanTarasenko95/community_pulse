from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
