from fastapi import APIRouter
from app.services.question_service import createQuestion,add_to_db, add_all_to_db, filter_questions_from_db, get_all_sections_from_db, get_all_question_types_from_db
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

@questionController.get("/sections", response_model=List[str])
async def get_all_sections():
    return await get_all_sections_from_db()

@questionController.get("/question_types", response_model=List[str])
async def get_all_question_types():
    return await get_all_question_types_from_db()