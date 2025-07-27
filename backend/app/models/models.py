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
    keywords: Optional[list[str]] = []  # Add keywords field to the model

    class Settings:
        name = "questions"  # Collection name
        
class KeywordModel(Document):
    keyword: str
    section: str
    questionType: str
    difficulty: int

    class Settings:
        name = "keywords"  # Collection name
        
        # index based on keyword for faster search
        # index based on section, questionType, and difficulty for filtering
        indexes = [
            {"fields": ["keyword"], "unique": True},
            {"fields": ["section", "questionType", "difficulty"]}
        ]   
