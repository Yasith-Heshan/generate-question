from pydantic import BaseModel, EmailStr
from typing import Optional, List
    
class QuestionCreate(BaseModel):
    section: str
    questionType: str
    difficulty: int
    description: str
    count: int
    
class QuestionResponse(BaseModel):
    questions: List[str]
    correctAnswers: List[str]
    mcqAnswers: Optional[List[str]]=[]
    section: str
    questionType: str
    difficulty: int
    
class Question(BaseModel):
    section: str
    questionType: str
    difficulty: int
    question: str
    correctAnswer: str
    mcqAnswers: Optional[List[str]] = []
