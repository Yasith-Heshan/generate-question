from fastapi import APIRouter
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from app.services.question_service import createQuestion, add_quetion_to_db
from app.schemas.question import QuestionCreate, QuestionResponse, Question
from app.adapters.db_adapter import SQLiteDBAdapter

router = APIRouter()

# Initialize the adapter with the path to your SQLite database file
db = SQLiteDBAdapter("my_database.db")
db.create_table(
    "questions",
    "id INTEGER PRIMARY KEY AUTOINCREMENT, section TEXT, questionType TEXT, difficulty INTEGER, question TEXT, correctAnswer TEXT, mcqAnswers TEXT"
)


@router.post("/users", response_model=UserResponse)
def register_user(user: UserCreate):
    return create_user(user)

@router.post("/questions", response_model=QuestionResponse)
def create_question(question: QuestionCreate):
    return createQuestion(question)

@router.post("/add_question", response_model=None)
def add_question_to_db(question: Question):
    add_question_to_db(question, db)
