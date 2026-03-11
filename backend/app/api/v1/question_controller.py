from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.services.question_service import (
    createQuestion,
    add_to_db,
    add_all_to_db,
    filter_questions_from_db,
    filter_questions_paginated,
    get_all_sections_from_db,
    get_keywords_by_filter,
    get_question_types_by_section,
    readContentFromImage,
    update_question_in_db,
)
from app.schemas.question import (
    QuestionGenerateRequestBody,
    QuestionResponseBody,
    Question,
    QuestionFilterRequestBody,
    PaginatedQuestionsResponse,
    TestRequestBody,
    QuestionUpdateRequestBody,
)
from typing import  List
from app.adapters.db_adapter import MongoDBAdapter

MongoDBAdapter.connect()
questionController = APIRouter()

@questionController.post("/questions", response_model=QuestionResponseBody, summary="Generate Questions", description="Generate mathematical questions based on the provided parameters", tags=["Question Generation"])
def create_question(question: QuestionGenerateRequestBody):
    return createQuestion(question)

@questionController.post("/add_question", summary="Add Single Question", description="Add a single question to the database", tags=["Database Management"])
async def add_question_to_db(question: Question):
    return await add_to_db(question)

@questionController.post("/add_all_questions", summary="Add Multiple Questions", description="Add multiple questions to the database", tags=["Database Management"])
async def add_all_questions_to_db(questions: List[Question]):
    return await add_all_to_db(questions)

@questionController.post("/filter_questions", response_model=List[Question], summary="Filter Questions", description="Filter questions from the database based on criteria", tags=["Query"])
async def filter_questions(questionFilterRequestBody: QuestionFilterRequestBody):
    # Existing frontend-facing endpoint returns a simple list
    return await filter_questions_from_db(questionFilterRequestBody)


@questionController.post(
    "/filter_questions_paginated",
    response_model=PaginatedQuestionsResponse,
    summary="Internal Paginated Filter",
    description="Internal endpoint providing paginated question results; not used by frontend",
    tags=["Internal"],
)
async def filter_questions_internal(questionFilterRequestBody: QuestionFilterRequestBody):
    return await filter_questions_paginated(questionFilterRequestBody)

@questionController.put("/questions/{question_id}", summary="Update Question", description="Update an existing question in the database", tags=["Database Management"])
async def update_question(question_id: str, update_data: QuestionUpdateRequestBody):
    return await update_question_in_db(question_id, update_data)

@questionController.get("/sections", response_model=List[str], summary="Get All Sections", description="Retrieve all available question sections", tags=["Metadata"])
async def get_all_sections():
    return await MongoDBAdapter.distinct_query('questions', 'section')

@questionController.delete("/questions/{question_id}")
async def delete(question_id):
    db = MongoDBAdapter.get_db()
    x=ObjectId(question_id)
    result = await db["questions"].delete_one({"_id": x})

    if result.deleted_count == 0:
        print('not found')
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}

@questionController.get("/keywords/filter", response_model=List[str], summary="Get Keywords by Filter", description="Get keywords filtered by section, question type, and difficulty", tags=["Metadata"])
async def get_keywords_filtered(section: str = None, questionType: str = None, difficulty: int = None):
    return await get_keywords_by_filter(section, questionType, difficulty)

@questionController.get("/question_types/filter", response_model=List[str], summary="Get Question Types by Section", description="Get question types filtered by section", tags=["Metadata"])
async def get_question_types_filtered(section: str = None):
    return await get_question_types_by_section(section)

@questionController.post("/test", response_model=str, summary="Test Image Processing", description="Test endpoint for processing images", tags=["Testing"])
def get_all_questions(testRequestBody: TestRequestBody):
    return readContentFromImage(testRequestBody.img)