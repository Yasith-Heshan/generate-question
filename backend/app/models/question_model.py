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
    keywords: Optional[list[str]] = []
    responseId: Optional[str] = None
    graphImg: Optional[str] = None
    userId: Optional[str] = None

    class Settings:
        name = "questions"  # Collection name
