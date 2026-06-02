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
from typing import List, Optional
from app.adapters.db_adapter import MongoDBAdapter
from datetime import datetime
from pydantic import BaseModel, Field

MongoDBAdapter.connect()

questionController = APIRouter()


# Response models for statistics
class QuestionTypeQuestionStat(BaseModel):
    questionType: str
    count: int


class SectionQuestionStat(BaseModel):
    section: str
    count: int
    questionTypeStats: List[QuestionTypeQuestionStat] = Field(default_factory=list)


class UserQuestionStat(BaseModel):
    userId: Optional[str]
    username: str = "Anonymous"
    count: int
    sectionStats: List[SectionQuestionStat] = Field(default_factory=list)


class QuestionStatisticsResponse(BaseModel):
    userStats: List[UserQuestionStat]
    totalQuestions: int


@questionController.post(
    "/questions",
    response_model=QuestionResponseBody,
    summary="Generate Questions",
    description="Generate mathematical questions based on the provided parameters",
    tags=["Question Generation"],
)
def create_question(question: QuestionGenerateRequestBody):
    return createQuestion(question)


@questionController.post(
    "/add_question",
    summary="Add Single Question",
    description="Add a single question to the database",
    tags=["Database Management"],
)
async def add_question_to_db(question: Question):
    return await add_to_db(question)


@questionController.post(
    "/add_all_questions",
    summary="Add Multiple Questions",
    description="Add multiple questions to the database",
    tags=["Database Management"],
)
async def add_all_questions_to_db(questions: List[Question]):
    return await add_all_to_db(questions)


@questionController.post(
    "/filter_questions",
    response_model=List[Question],
    summary="Filter Questions",
    description="Filter questions from the database based on criteria",
    tags=["Query"],
)
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
async def filter_questions_internal(
    questionFilterRequestBody: QuestionFilterRequestBody,
):
    return await filter_questions_paginated(questionFilterRequestBody)


@questionController.put(
    "/questions/{question_id}",
    summary="Update Question",
    description="Update an existing question in the database",
    tags=["Database Management"],
)
async def update_question(question_id: str, update_data: QuestionUpdateRequestBody):
    return await update_question_in_db(question_id, update_data)


@questionController.get(
    "/sections",
    response_model=List[str],
    summary="Get All Sections",
    description="Retrieve all available question sections",
    tags=["Metadata"],
)
async def get_all_sections():
    return await MongoDBAdapter.distinct_query("questions", "section")


@questionController.put("/questions/{question_id}/restore")
async def restore(question_id):
    db = MongoDBAdapter.get_db()
    x = ObjectId(question_id)
    # First check if the question exists
    question = await db["questions"].find_one({"_id": x})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # If not deleted, return success
    if not question.get("deleted", False):
        return {"message": "Question is already active"}

    # Set deleted to False
    result = await db["questions"].update_one({"_id": x}, {"$set": {"deleted": False}})
    return {"message": "Question restored successfully"}


@questionController.delete("/questions/{question_id}")
async def delete_question(question_id: str):
    print(f"Attempting to delete question with ID: {question_id}")
    db = MongoDBAdapter.get_db()
    try:
        x = ObjectId(question_id)
    except Exception as e:
        print(f"Invalid ObjectId: {question_id}, error: {e}")
        raise HTTPException(status_code=400, detail="Invalid question ID")

    # First check if the question exists
    question = await db["questions"].find_one({"_id": x})
    print(f"Question found: {question is not None}")
    if question:
        print(f"Question deleted status: {question.get('deleted', 'not set')}")

    if not question:
        print("Question not found")
        raise HTTPException(status_code=404, detail="Question not found")

    # If already deleted, return success
    if question.get("deleted", False):
        print("Question already deleted")
        return {"message": "Question is already deleted"}

    # Set deleted to True
    result = await db["questions"].update_one({"_id": x}, {"$set": {"deleted": True}})
    print(f"Update result: {result.modified_count} documents modified")
    return {"message": "Question deleted successfully"}


@questionController.get(
    "/keywords/filter",
    response_model=List[str],
    summary="Get Keywords by Filter",
    description="Get keywords filtered by section, question type, and difficulty",
    tags=["Metadata"],
)
async def get_keywords_filtered(
    section: str = None, questionType: str = None, difficulty: int = None
):
    return await get_keywords_by_filter(section, questionType, difficulty)


@questionController.get(
    "/question_types/filter",
    response_model=List[str],
    summary="Get Question Types by Section",
    description="Get question types filtered by section",
    tags=["Metadata"],
)
async def get_question_types_filtered(section: str = None):
    return await get_question_types_by_section(section)


@questionController.get(
    "/statistics",
    response_model=QuestionStatisticsResponse,
    summary="Get Question Statistics",
    description="Get statistics about questions by user with optional filtering",
    tags=["Statistics"],
)
async def get_statistics(
    user_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """
    Get question statistics grouped by user.

    Parameters:
    - user_id: Optional user ID to filter by specific user
    - start_date: Optional start date (ISO format: YYYY-MM-DD)
    - end_date: Optional end date (ISO format: YYYY-MM-DD)
    """
    db = MongoDBAdapter.get_db()
    questions_collection = db["questions"]

    # Build filter
    filter_query = {"is_deleted": False}

    # Add user filter if provided
    if user_id:
        filter_query["userId"] = user_id

    # Add date range filter if provided
    if start_date or end_date:
        date_filter = {}
        if start_date:
            try:
                start = datetime.fromisoformat(start_date)
                date_filter["$gte"] = start
            except:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid start_date format. Use ISO format: YYYY-MM-DD",
                )
        if end_date:
            try:
                end = datetime.fromisoformat(end_date)
                date_filter["$lte"] = end
            except:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid end_date format. Use ISO format: YYYY-MM-DD",
                )

        if date_filter:
            filter_query["createdAt"] = date_filter

    # Aggregate counts by user, section, and question type
    pipeline = [
        {"$match": filter_query},
        {
            "$facet": {
                "userCounts": [
                    {"$group": {"_id": "$userId", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                ],
                "sectionCounts": [
                    {
                        "$group": {
                            "_id": {"userId": "$userId", "section": "$section"},
                            "count": {"$sum": 1},
                        }
                    },
                    {"$sort": {"count": -1}},
                ],
                "typeCounts": [
                    {
                        "$group": {
                            "_id": {
                                "userId": "$userId",
                                "section": "$section",
                                "questionType": "$questionType",
                            },
                            "count": {"$sum": 1},
                        }
                    },
                    {"$sort": {"count": -1}},
                ],
            }
        },
    ]

    aggregation_results = await questions_collection.aggregate(pipeline).to_list(None)
    if not aggregation_results:
        aggregation_results = [
            {"userCounts": [], "sectionCounts": [], "typeCounts": []}
        ]

    result_set = aggregation_results[0]
    user_counts = result_set.get("userCounts", [])
    section_counts = result_set.get("sectionCounts", [])
    type_counts = result_set.get("typeCounts", [])

    section_by_user: dict = {}
    for section_result in section_counts:
        user_id_val = section_result.get("_id", {}).get("userId")
        section_name = section_result.get("_id", {}).get("section") or "Unknown"
        if user_id_val not in section_by_user:
            section_by_user[user_id_val] = {}
        section_by_user[user_id_val][section_name] = SectionQuestionStat(
            section=section_name,
            count=section_result.get("count", 0),
        )

    for type_result in type_counts:
        user_id_val = type_result.get("_id", {}).get("userId")
        section_name = type_result.get("_id", {}).get("section") or "Unknown"
        question_type = type_result.get("_id", {}).get("questionType") or "Unknown"
        user_sections = section_by_user.setdefault(user_id_val, {})
        if section_name not in user_sections:
            user_sections[section_name] = SectionQuestionStat(
                section=section_name,
                count=0,
            )
        user_sections[section_name].questionTypeStats.append(
            QuestionTypeQuestionStat(
                questionType=question_type, count=type_result.get("count", 0)
            )
        )

    # Get total count
    total_count = await questions_collection.count_documents(filter_query)

    # Format results
    user_stats = []
    for result in user_counts:
        user_id_val = result.get("_id")
        user_stats.append(
            UserQuestionStat(
                userId=user_id_val,
                username=user_id_val or "Anonymous",
                count=result.get("count", 0),
                sectionStats=list(section_by_user.get(user_id_val, {}).values()),
            )
        )

    return QuestionStatisticsResponse(userStats=user_stats, totalQuestions=total_count)


@questionController.post(
    "/test",
    response_model=str,
    summary="Test Image Processing",
    description="Test endpoint for processing images",
    tags=["Testing"],
)
def get_all_questions(testRequestBody: TestRequestBody):
    return readContentFromImage(testRequestBody.img)
