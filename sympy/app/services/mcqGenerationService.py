from typing import List
from app.models.dataModels import ServiceResponce
from app.services.question_generation_factory import QuestionGeneratorFactory

special_mcq_counts = {
    "22_E_1__2_27": [3,3,3]
}
1
def generateMcqQuestions(section: str,
                    question_type: str,
                    difficulty: int,
                    questions_count: int
                    ):
    # Code to generate MCQ questions
    responses:List[ServiceResponce]  = []
    service = QuestionGeneratorFactory.get_service(section, question_type, difficulty, questions_count)
    questionsAndAnswers:List[ServiceResponce] = service.generate_questions(question_type)
    for question in questionsAndAnswers:
        consideringQuestion = question.question
        correctAnswer = question.correct_solution
        allAnswers = [correctAnswer]
        if((question.other_solutions is not None)):
            otherAnswers = question.other_solutions
        else:
            mcq_count = 5
            if question_type in special_mcq_counts:
                if len(special_mcq_counts[question_type]) > 0:
                    mcq_count = special_mcq_counts[question_type][difficulty-1]
                else:
                    mcq_count = special_mcq_counts[question_type][0] 
            mcq_count_to_generate = mcq_count
            maximum_tries = 30
            while mcq_count_to_generate > 0:
                service = QuestionGeneratorFactory.get_service(section, question_type, difficulty, mcq_count_to_generate)
                otherQuestions = service.generate_questions(question_type)
                for otherQuestion in otherQuestions:
                    if otherQuestion.correct_solution not in allAnswers:
                        allAnswers.append(otherQuestion.correct_solution)
                mcq_count_to_generate = mcq_count - len(allAnswers)
                maximum_tries -= 1
                if maximum_tries < 0:
                    break
            
            otherAnswers = allAnswers[1:mcq_count]
            
                
                
                
        serviceResponse = ServiceResponce(consideringQuestion, correctAnswer, otherAnswers,question.graph_img)
        responses.append(serviceResponse)

        
    return responses
    

    