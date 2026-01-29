from app.services.Book22Chaptor02.problem_type_22_E_2__4_11 import generate_problem_22_E_2__4_11_questions
from app.services.Book22Chaptor02.problem_type_22_E_2__3_21 import generate_22_E_2__3_21_questions
from app.services.Book22Chaptor02.problem_type_22_E_2__5_07 import generate_22_E_2__5_07_questions
from app.services.Book22Chaptor02.problem_type_22_E_2__4_35 import generate_22_E_2__4_35_questions
from app.services.Book22Chaptor02.problem_type_22_E_2__5_05 import generate_problem_22_E_2__5_05_questions
from app.services.base_quetion_generator_service import BaseQuestionGeneratorService
from app.models.dataModels import ServiceResponce
from typing import List
from app.services.Book22Chaptor02.problem_type_22_E_2__2__01 import generate_problem_22_E_2__2_01_questions
from app.services.Book22Chaptor02.problem_type_22_E_2__4_62 import generate_problem_22_E_2__4_62_questions

class Book22Chaptor02Service(BaseQuestionGeneratorService):
    def generate_answers(self) -> list:
        pass

    def format_questions(self):
        pass
    def generate_22_E_2__2_01_questions(self,
                                        difficulty: int,
                                        questions_count: int)->List[ServiceResponce]:
        questions_and_solutions =  generate_problem_22_E_2__2_01_questions(difficulty, questions_count)
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'], other_solutions=x['other_solutions']), questions_and_solutions))
        
        return questions_and_answers
    
    def generate_22_E_2__4_11_questions(self,
                                        difficulty: int,
                                        questions_count: int)->List[ServiceResponce]:
        questions_and_solutions =  generate_problem_22_E_2__4_11_questions(difficulty, questions_count)
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'], other_solutions=x["other_solutions"]), questions_and_solutions))
        
        return questions_and_answers    
    
    def generate_22_E_2__5_05_questions(self,
                                        difficulty: int,
                                        questions_count: int)->List[ServiceResponce]:
        questions_and_solutions =  generate_problem_22_E_2__5_05_questions(difficulty, questions_count)
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'], other_solutions=x["other_solutions"],graph_img=x["graph_img"]), questions_and_solutions))
        
        return questions_and_answers
    
    def generate_22_E_2__4_62_questions(self,
                                        difficulty: int,
                                        questions_count: int)->List[ServiceResponce]:
        questions_and_solutions =  generate_problem_22_E_2__4_62_questions(difficulty, questions_count)
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'], other_solutions=x["other_solutions"],graph_img=x["graph_img"]), questions_and_solutions))
        
        return questions_and_answers