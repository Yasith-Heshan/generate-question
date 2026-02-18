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
    responseId: Optional[str] = None  # Response identifier from AI generation
    is_deleted: Optional[bool] = False

    class Settings:
        name = "questions"  # Collection name
        
class KeywordModel(Document):
    keyword: str
    section: str
    questionType: str
    difficulty: int

    class Settings:
        name = "keywords"  # Collection name
        
        # Fixed index configuration
        indexes = [
            "keyword",  # Simple index on keyword field
            [("section", 1), ("questionType", 1), ("difficulty", 1)]  # Compound index
        ]
