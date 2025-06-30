from pydantic import BaseModel
from typing import Optional, List
    
class QuestionGenerateRequestBody(BaseModel):
    section: str
    questionType: str
    difficulty: int
    description: str
    count: int
    exampleQuestion: Optional[str] = None  # Optional field for an example question
    
class QuestionResponseBody(BaseModel):
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
    
class QuestionFilterRequestBody(BaseModel):
    section:Optional[str] = None
    questionType: Optional[str] = None
    difficulty: Optional[int] = None
    
    
