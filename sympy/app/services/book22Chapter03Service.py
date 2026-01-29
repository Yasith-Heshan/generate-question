from typing import List

from app.models.dataModels import ServiceResponce
from app.services.Book22Chaptor03.problem_type_22_3__3_01 import generate_problem_22_E_3__3_01_questions
from app.services.Book22Chaptor03.problem_type_22_E_3_2_27 import generate_problem_22_E_3__2_27_questions
from app.services.Book22Chaptor03.problem_type_22_E_3__3_07 import generate_problem_22_E_3__3_07_questions
from app.services.base_quetion_generator_service import BaseQuestionGeneratorService


class Book22Chaptor03Service(BaseQuestionGeneratorService):
    def generate_answers(self) -> list:
        pass

    def format_questions(self):
        pass
    def generate_22_E_3__3_01_questions(self,
                                        difficulty: int,
                                        questions_count: int)->List[ServiceResponce]:
        questions_and_solutions =  generate_problem_22_E_3__3_01_questions(difficulty, questions_count)
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'], other_solutions=x['other_solutions']), questions_and_solutions))
        
        return questions_and_answers

    def generate_22_E_3__3_07_questions(self,
                                        difficulty: int,
                                        questions_count: int) -> List[ServiceResponce]:
        questions_and_solutions = generate_problem_22_E_3__3_07_questions(difficulty, questions_count)
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'],
                                          other_solutions=x['other_solutions']), questions_and_solutions))

        return questions_and_answers
    
    def generate_22_E_3__2_27_questions(self,
                                        difficulty: int,
                                        questions_count: int) -> List[ServiceResponce]:
        questions_and_solutions = generate_problem_22_E_3__2_27_questions(difficulty, questions_count)
       
        return questions_and_solutions