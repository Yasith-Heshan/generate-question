from fastapi import APIRouter
from app.services.user_service import create_user
from app.services.question_service import createQuestion,add_to_db, add_all_to_db, filter_questions_from_db
from app.schemas.question import QuestionGenerateRequestBody, QuestionResponseBody, Question, QuestionFilterRequestBody
from typing import  List

questionController = APIRouter()

@questionController.post("/questions", response_model=QuestionResponseBody)
def create_question(question: QuestionGenerateRequestBody):
    return createQuestion(question)

@questionController.post("/add_question", response_model=None)
async def add_question_to_db(question: Question):
    return await add_to_db(question)

@questionController.post("/add_all_questions", response_model=None)
async def add_all_questions_to_db(questions: List[Question]):
    return await add_all_to_db(questions)

@questionController.post("/filter_questions", response_model=List[Question])
async def filter_questions(questionFilterRequestBody: QuestionFilterRequestBody):
    return await filter_questions_from_db(questionFilterRequestBody)
    
