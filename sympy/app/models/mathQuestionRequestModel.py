from pydantic import BaseModel


class RequestModel(BaseModel):
    # Define fields that may change over time
    section: str
    question_type: str
    difficulty: int
    questions_count: int
    mcq: bool
