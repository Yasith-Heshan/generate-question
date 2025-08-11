from fastapi import APIRouter
from app.services.question_service import createQuestion,add_to_db, add_all_to_db, filter_questions_from_db, get_all_sections_from_db, get_keywords_by_filter, get_question_types_by_section, readContentFromImage
from app.schemas.question import QuestionGenerateRequestBody, QuestionResponseBody, Question, QuestionFilterRequestBody, TestRequestBody
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

@questionController.get("/keywords/filter", response_model=List[str])
async def get_keywords_filtered(section: str = None, questionType: str = None, difficulty: int = None):
    return await get_keywords_by_filter(section, questionType, difficulty)

@questionController.get("/question_types/filter", response_model=List[str])
async def get_question_types_filtered(section: str = None):
    return await get_question_types_by_section(section)

@questionController.post("/test", response_model=str)
def get_all_questions(testRequestBody: TestRequestBody):
    return readContentFromImage(testRequestBody.img)