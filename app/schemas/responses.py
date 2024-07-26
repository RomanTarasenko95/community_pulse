from pydantic import BaseModel, Field


class ResponseCreate(BaseModel):
    question_id: int = Field(..., description='Question id')
    is_agree: bool = Field(..., description='Agree or disagree flag')


class StatisticResponse(BaseModel):
    question_id: int
    agree_count: int
    disagree_count: int
