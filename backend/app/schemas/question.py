from pydantic import BaseModel
from typing import Optional, List
    
class QuestionGenerateRequestBody(BaseModel):
    section: str
    questionType: str
    difficulty: int
    description: str
    count: int
    image: Optional[str] = None  # Optional field for image content
    detailedAnswer: Optional[bool] = False  # Optional field to indicate if detailed answer is required
    exampleQuestion: Optional[str] = None  # Optional field for an example question
    prevResponseId: Optional[str] = None  # Optional field for request ID
    keywords: Optional[List[str]] = []  # Optional field for keywords associated with the question
    
class QuestionResponseBody(BaseModel):
    questions: List[str]
    detailedAnswers: Optional[List[str]] = None  # Optional field for detailed answer
    correctAnswers: List[str]
    mcqAnswers: Optional[List[str]]=[]
    section: str
    questionType: str
    difficulty: int
    keywords: Optional[List[str]] = []  # Optional field for keywords associated with the question
    responseId: str  # Optional field for response ID
    
class Question(BaseModel):
    section: str
    questionType: str
    difficulty: int
    question: str
    correctAnswer: str
    detailedAnswer: Optional[str] = None
    mcqAnswers: Optional[List[str]] = []
    keywords: Optional[List[str]] = []  # Optional field for keywords associated with the question
    
class QuestionFilterRequestBody(BaseModel):
    section:Optional[str] = None
    questionType: Optional[str] = None
    difficulty: Optional[int] = None
    keywords: Optional[List[str]] = []
    
    
class TestRequestBody(BaseModel):
    img: str  # Assuming the image is passed as a base64 string or a URL