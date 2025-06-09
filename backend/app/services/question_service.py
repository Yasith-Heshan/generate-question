from app.schemas.question import QuestionCreate, QuestionResponse, Question
import openai
from dotenv import load_dotenv
import os
import re
from app.adapters.db_adapter import SQLiteDBAdapter
import sqlite3

# Load environment variables from .env file
load_dotenv()


# Get API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()


def extract_questions(text):
    """
    Extracts all questions from the given text that follow the format:
    'Question: <question>'
    Returns a list of question strings.
    """
    pattern = r"Question:\s*(.*?)(?=\nAnswer:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    # Strip whitespace from each question
    return [q.strip() for q in matches]

def extract_answers(text):
    """
    Extracts all answers from the given text that follow the format:
    'Answer: <answer>'
    Returns a list of answer strings.
    """
    pattern = r"Answer:\s*(.*?)(?=\nMCQ_Answers:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    # Strip whitespace from each answer
    return [a.strip() for a in matches]

def extract_mcq_answers(text):
    """
    Extracts all mcq answers from the given text that follow the format:
    'MCQ_Answers: <mcq_answers>'
    Returns a list of mcq answer strings.
    """
    pattern = r"MCQ_Answers:\s*(.*?)(?=\n\nQuestion:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    # Strip whitespace from each mcq answer
    return [a.strip() for a in matches]


def generate_math_word_problem(question_description,count=1):
    
    # Define the math prompt
    math_problem_count = "a math problem" if count == 1 else f"{count} math problems"
    math_prompt = f"""
    Create {math_problem_count} according to the following description:
    {question_description}
    Give only the question, answer and suitable 4 mcq asnwers other than the correct answer.
    MCQ answers should be in the format: MCQ_Answers: [<mcq_answer1>, <mcq_answer2>, <mcq_answer3>, <mcq_answer4>]
    Use different letters for the variable: x, y, t, u, v, z, r, s (choose the variable randomly) and f, g, h, p, q, r for the function names.
    Make sure that they do not evaluate to negative square roots, logs of negative numbers, etc.
    Always use latex for math expressions (Use \\left( and  \\right) for parenthesis). Use the format:
    Question: <question>
    Answer: <answer>
    MCQ_Answers: <mcq_answers_list>\\n
    """

    response = client.responses.create(
        model="gpt-4.1",
        # reasoning={"effort": "medium"},
        input=math_prompt,
    )
    # extract the generated question from the response
    questions = extract_questions(response.output_text)
    answers = extract_answers(response.output_text)
    mcq_answers = extract_mcq_answers(response.output_text)
    return questions,answers, mcq_answers




def createQuestion(requestBody: QuestionCreate) -> QuestionResponse:
    description = requestBody.description
    count = requestBody.count
    section = requestBody.section
    questionType = requestBody.questionType
    difficulty = requestBody.difficulty
    questions, answers, mcq_answers = generate_math_word_problem(description, count)
    questionResponse = QuestionResponse(
        questions=questions,
        correctAnswers=answers,
        mcqAnswers=mcq_answers,
        section=section,
        questionType=questionType,
        difficulty=difficulty
    )
    return questionResponse
    
def add_quetion_to_db(requestBody: Question, db:sqlite3.Connection ) -> None:
    try:
        db.add_question(
            section=requestBody.section,
            question_type=requestBody.questionType,
            difficulty=requestBody.difficulty,
            question=requestBody.question,
            correctAnswer=requestBody.correctAnswer,
            mcqAnswers=requestBody.mcqAnswers or []
        )
    except exception as e:
        print(f"An error occurred while adding the question to the database: {e}")
        raise e
    