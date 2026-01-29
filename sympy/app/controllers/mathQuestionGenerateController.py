from typing import List
from app.models.mathQuestionRequestModel import RequestModel
from app.models.dataModels import ServiceResponce
from app.services import mcqGenerationService
from app.services.question_generation_factory import QuestionGeneratorFactory

from app.services.pdfCreationService import create_pdf

def generateMathQuestion(request: RequestModel):
   
    if request.mcq:
        questionsAndSolutions = mcqGenerationService.generateMcqQuestions(
            request.section,
            request.question_type,
            request.difficulty,
            request.questions_count,
        )
        return questionsAndSolutions
    else:
        service = QuestionGeneratorFactory.get_service(request.section,
            request.question_type,
            request.difficulty,
            request.questions_count
            )
        questionsAndSolutions:List[ServiceResponce] =  service.generate_questions(request.question_type)
        questionsAndSolutions = list(map(lambda x: ServiceResponce(question=x.question, correct_solution=x.correct_solution, other_solutions=None, graph_img=x.graph_img), questionsAndSolutions))
        return questionsAndSolutions
