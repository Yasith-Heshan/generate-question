from typing import Dict, Type

from app.services.book22Chaptor01Service import (
    Book22Chaptor01Service,
)
from app.services.book22Chaptor02Service import (
    Book22Chaptor02Service,
)
from app.services.base_quetion_generator_service import BaseQuestionGeneratorService
from app.services.book22Chapter03Service import (
    Book22Chaptor03Service,
)



class QuestionGeneratorFactory:

    _services: Dict[str, Type[BaseQuestionGeneratorService]] = {
        "B22_Ch01": Book22Chaptor01Service,
        "B22_Ch02": Book22Chaptor02Service,
        "B22_Ch03": Book22Chaptor03Service,
        # add other qeuestion generation services
    }

    @staticmethod
    def get_service(section: str,
                    question_type: str,
                    difficulty: int,
                    questions_count: int) -> BaseQuestionGeneratorService:
        service_class = QuestionGeneratorFactory._services.get(section)
        if not service_class:
            raise ValueError
        (f"No question generator available for section: {section}")

        return service_class(questions_count = questions_count, difficulty = difficulty)
