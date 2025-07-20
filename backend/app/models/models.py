from beanie import Document
from typing import Optional

class QuestionModel(Document):
    section: str
    questionType: str
    difficulty: int
    question: str
    correctAnswer: str
    detailedAnswer: Optional[str] = None
    mcqAnswers: Optional[list[str]] = []

    class Settings:
        name = "questions"  # Collection name
        
class KeywordModel(Document):
    keyword: str
    questionType: str
    difficulty: int

    class Settings:
        name = "keywords"  # Collection name
