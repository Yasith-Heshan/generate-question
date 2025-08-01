from app.schemas.question import QuestionGenerateRequestBody, QuestionResponseBody,Question, QuestionFilterRequestBody
import openai
from dotenv import load_dotenv
import os
import re
from fastapi import HTTPException
from app.models.models import QuestionModel, KeywordModel


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

def get_detailed_answers(questions: list[str]):
    """
    generates detailed answers for a list of questions using the OpenAI API."""
    detailed_answers = []
    for question in questions:
        prompt = f"Provide a detailed answer for the following question:\n{question}"
        response = client.responses.create(
            model="gpt-4.1",
            input=prompt,
        )
        detailed_answers.append(response.output_text.strip())
    return detailed_answers if detailed_answers else []

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


def generate_math_word_problem(question_description,count=1,example_question=None, image=None, prevResponseId=None):
    imageToText = ""
    if image:
        imageToText = readContentFromImage(image)
        if not imageToText:
            raise HTTPException(status_code=400, detail="Failed to read content from image.")
    # Define the math prompt
    math_problem_count = "a math problem" if count == 1 else f"{count} math problems"
    math_prompt = f"""
    Create {math_problem_count} according to the following description:
    {question_description}
    {imageToText if image else ""}
    {"Example question: " + example_question if example_question else ""}
    {"Generate question in the same format as the previous response." if prevResponseId else ""}
    Give only the question, answer and suitable 4 mcq asnwers other than the correct answer.
    MCQ answers should be in the format: MCQ_Answers: [<mcq_answer1>, <mcq_answer2>, <mcq_answer3>, <mcq_answer4>]
    Use different letters for the variable: x, y, t, u, v, z, r, s (choose the variable randomly) and f, g, h, p, q, r for the function names.
    Make sure that they do not evaluate to negative square roots, logs of negative numbers, etc.
    Always use latex for math expressions (Use \\left( and  \\right) for parenthesis). Use the format:
    Question: <question>
    Detailed_Answer: <detailed_answer> (if detailed_answer is True)
    Answer: <answer>
    MCQ_Answers: <mcq_answers_list>\\n
    """

    response = client.responses.create(
        model="gpt-4.1",
        # reasoning={"effort": "medium"},
        input=math_prompt,
        previous_response_id=prevResponseId,  # Use the previous response ID if provided
    )
    
    
    # extract the generated question from the response
    questions = extract_questions(response.output_text)
    answers = extract_answers(response.output_text)
    mcq_answers = extract_mcq_answers(response.output_text)
    return questions,answers, mcq_answers, response.id

def readContentFromImage(imageBase64: str) -> str:
    """
    Reads content from an image using OpenAI's OCR capabilities.

    Args:
        imageBase64 (str): Base64-encoded image string.

    Returns:
        str: Extracted text from the image.
    """
    try:
        # extract the base64 string from the imageBase64
        if imageBase64.startswith("data:image/"):
            imageBase64 = imageBase64.split(",")[1]
        # Send the image to GPT-4 Vision model
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{imageBase64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Read and extract all visible text from this image."
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"



def createQuestion(requestBody: QuestionGenerateRequestBody) -> QuestionResponseBody:
    description = requestBody.description
    count = requestBody.count
    detailed_Answer = requestBody.detailedAnswer
    section = requestBody.section
    questionType = requestBody.questionType
    difficulty = requestBody.difficulty
    try:
        questions, answers, mcq_answers,responseId = generate_math_word_problem(description, count, requestBody.exampleQuestion,requestBody.image,requestBody.prevResponseId)
        detailed_answers = get_detailed_answers(questions) if detailed_Answer else []
        questionResponse = QuestionResponseBody(
            questions=questions,
            detailedAnswers=detailed_answers if detailed_Answer else None,
            correctAnswers=answers,
            mcqAnswers=mcq_answers,
            section=section,
            questionType=questionType,
            difficulty=difficulty,
            keywords=requestBody.keywords if requestBody.keywords else [],
            responseId=responseId
        )
        return questionResponse
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    
async def add_keywords_to_db(keywords: list[str], section: str, questionType: str, difficulty: int):
    """
    Add keywords to the keywords collection. 
    Only inserts keywords that don't already exist to maintain uniqueness.
    """
    try:
        for keyword in keywords:
            # Check if keyword already exists
            existing_keyword = await KeywordModel.find_one({"keyword": keyword})
            if not existing_keyword:
                keyword_doc = KeywordModel(
                    keyword=keyword,
                    section=section,
                    questionType=questionType,
                    difficulty=difficulty
                )
                await keyword_doc.insert()
    except Exception as e:
        # Log the error but don't fail the question insertion
        print(f"Error inserting keywords: {str(e)}")

async def add_to_db(
    question: Question
):
    try:
        doc= QuestionModel(**question.dict())
        await doc.insert()
        
        # Insert keywords if they exist
        if question.keywords:
            await add_keywords_to_db(
                keywords=question.keywords,
                section=question.section,
                questionType=question.questionType,
                difficulty=question.difficulty
            )
        
        return {"message": "Question added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
async def add_all_to_db(questions: list[Question]):
    try:
        await QuestionModel.insert_many([QuestionModel(**q.dict()) for q in questions])
        
        # Insert keywords for all questions
        for question in questions:
            if question.keywords:
                await add_keywords_to_db(
                    keywords=question.keywords,
                    section=question.section,
                    questionType=question.questionType,
                    difficulty=question.difficulty
                )
        
        return {"message": "All questions added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
async def filter_questions_from_db(questionFilterRequestBody: QuestionFilterRequestBody):
    try:
        filters = {}

        if questionFilterRequestBody.section:
            filters["section"] = questionFilterRequestBody.section
        if questionFilterRequestBody.questionType:
            filters["questionType"] = questionFilterRequestBody.questionType
        if questionFilterRequestBody.difficulty is not None:
            filters["difficulty"] = questionFilterRequestBody.difficulty
        if questionFilterRequestBody.keywords:
            filters["keywords"] = {"$in": questionFilterRequestBody.keywords}
        questions = await QuestionModel.find(filters).to_list()
        return questions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
async def get_all_sections_from_db():
    try:
        sections = await KeywordModel.get_motor_collection().distinct("section")
        return sections
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
async def get_all_question_types_from_db():
    try:
        question_types = await KeywordModel.get_motor_collection().distinct("questionType")
        return question_types
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_all_keywords_from_db():
    """
    Get all unique keywords from the keywords collection.
    """
    try:
        keywords = await KeywordModel.get_motor_collection().distinct("keyword")
        return keywords
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_keywords_by_filter(section: str = None, questionType: str = None, difficulty: int = None):
    """
    Get keywords filtered by section, questionType, and/or difficulty.
    """
    try:
        filters = {}
        if section:
            filters["section"] = section
        if questionType:
            filters["questionType"] = questionType
        if difficulty is not None:
            filters["difficulty"] = difficulty
        
        keywords = await KeywordModel.find(filters).to_list()
        return [keyword.keyword for keyword in keywords]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_question_types_by_section(section: str = None):
    """
    Get question types filtered by section.
    """
    try:
        filters = {}
        if section:
            filters["section"] = section
        
        question_types = await KeywordModel.get_motor_collection().distinct("questionType", filters)
        return question_types
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))