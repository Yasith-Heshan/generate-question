from app.schemas.question import QuestionGenerateRequestBody, QuestionResponseBody,Question, QuestionFilterRequestBody, QuestionUpdateRequestBody
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
    pattern = r"Question:\s*(.*?)(?=\nDetailed_Answer:|\nAnswer:|\Z)"
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
    Returns a list of answer strings (only the final answer value, not the full solution).
    """
    # Extract everything from "Answer:" until "MCQ_Answers:" or end of string
    pattern = r"Answer:\s*(.*?)(?=\nMCQ_Answers:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    
    final_answers = []
    for match in matches:
        # Clean up the match and extract only the numerical answer
        lines = match.strip().split('\n')
        # Look for the line that contains a percentage or number (the final answer)
        for line in reversed(lines):  # Start from the end to get the final answer
            line = line.strip()
            if line and (re.search(r'^\d+\.?\d*%?$', line) or re.search(r'^\d+\.\d+%$', line) or re.search(r'^\d+%$', line)):
                final_answers.append(line)
                break
        else:
            # If no clear numerical answer found, take the last non-empty line
            for line in reversed(lines):
                line = line.strip()
                if line:
                    final_answers.append(line)
                    break
    
    return final_answers

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
    Create {math_problem_count} based on the following requirements:

    DESCRIPTION: {question_description}
    {imageToText if image else ""}
    {"EXAMPLE TO FOLLOW: " + example_question if example_question else ""}
    {"IMPORTANT: Generate questions in the exact same format and style as the previous response." if prevResponseId else ""}

    MATHEMATICAL REQUIREMENTS:
    - Ensure all mathematical expressions are valid and well-defined
    - Avoid operations that lead to undefined results (negative square roots, logarithms of negative numbers, division by zero, etc.)
    - Use realistic and reasonable numerical values that make sense in context
    - Verify that all calculations are mathematically sound

    VARIABLE AND FUNCTION NAMING:
    - Variables: Choose randomly from x, y, t, u, v, z, r, s (use different variables for variety)
    - Functions: Choose randomly from f, g, h, p, q, r (use different function names for variety)
    - Ensure variable names are contextually appropriate

    MCQ ANSWER REQUIREMENTS:
    - Generate exactly 4 incorrect multiple-choice options that are plausible but wrong
    - Make incorrect answers mathematically reasonable (not obviously wrong)
    - Ensure incorrect answers are distinct from each other and the correct answer
    - Use similar formatting and units as the correct answer

    FORMATTING REQUIREMENTS:
    - Use LaTeX for ALL mathematical expressions (equations, formulas, numbers with operations)
    - Use \\left( and \\right) for parentheses in LaTeX
    - Ensure proper LaTeX syntax for fractions, exponents, radicals, etc.
    - Keep consistent spacing and formatting throughout

    OUTPUT FORMAT (MUST FOLLOW EXACTLY):
    Question: <question>
    Detailed_Answer: <detailed_answer> (if detailed_answer is True)
    Answer: <final_answer_only> (Only the final numerical answer with units, no explanation or working)
    MCQ_Answers: [<mcq_answer1>, <mcq_answer2>, <mcq_answer3>, <mcq_answer4>]

    Generate ONLY the mathematical content following the exact format above. Do not include any explanatory text, headers, or additional formatting.
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
        if questionFilterRequestBody.id:
            from beanie import PydanticObjectId
            filters["_id"] = PydanticObjectId(questionFilterRequestBody.id)
        questions = await QuestionModel.find(filters).to_list()
        return questions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def update_question_in_db(question_id: str, update_data: QuestionUpdateRequestBody):
    """
    Update a question in the database by ID.
    """
    try:
        from beanie import PydanticObjectId
        
        # Convert string ID to ObjectId
        object_id = PydanticObjectId(question_id)
        
        # Find the question by ID
        question = await QuestionModel.get(object_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Get the update data as dict and filter out None values
        update_dict = update_data.dict(exclude_unset=True)
        
        # Update the question with the provided data
        for field, value in update_dict.items():
            if value is not None:
                setattr(question, field, value)
        
        # Save the updated question
        await question.save()
        
        # Handle keywords update if provided
        if 'keywords' in update_dict and update_dict['keywords'] is not None:
            # Get the updated question data
            section = getattr(question, 'section', None)
            question_type = getattr(question, 'questionType', None)
            difficulty = getattr(question, 'difficulty', None)
            
            if section and question_type and difficulty is not None:
                await add_keywords_to_db(
                    keywords=update_dict['keywords'],
                    section=section,
                    questionType=question_type,
                    difficulty=difficulty
                )
        
        return {"message": "Question updated successfully", "question": question}
    except Exception as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail="Question not found")
        raise HTTPException(status_code=400, detail=str(e))
    
async def get_all_sections_from_db():
    try:
        print("Attempting to get sections from database...")
        
        # Method 4: Using find with projection (most efficient for this setup)
        # Only fetch the section field to reduce data transfer
        keywords = await KeywordModel.find({}).to_list()
        sections = sorted(list(set([keyword.section for keyword in keywords])))
        
        # If still no sections found, return empty list instead of failing
        if not sections:
            print("No sections found in collection")
            return []
        
        print(f"Found sections: {sections}")
        return sections
    except Exception as e:
        print(f"Error getting sections: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

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
        
        # Use the same working pattern as other endpoints
        keywords = await KeywordModel.find(filters).to_list()
        question_types = sorted(list(set([keyword.questionType for keyword in keywords])))
        
        return question_types
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))