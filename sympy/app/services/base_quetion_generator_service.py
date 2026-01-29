from abc import ABC, abstractmethod
from typing import Callable, Dict, Type


# Base class for question generator service
class BaseQuestionGeneratorService(ABC):

    def __init__(self, difficulty: int, questions_count: int):
        self.difficulty = difficulty
        self.questions_count = questions_count


    def generate_questions(self, question_type: str) -> list:
        # Dynamically get the method for the given question type
        generate_method: Callable = getattr(self, f"generate_{question_type}_questions", None)
        return generate_method(self.difficulty, self.questions_count)

    @abstractmethod
    def generate_answers(self) -> list:
        pass

    @abstractmethod
    def format_questions(self):
        pass
