from fastapi import APIRouter, Depends, HTTPException, status
from app.models.dataModels import ServiceResponce
from app.models.mathQuestionRequestModel import RequestModel
from app.controllers.mathQuestionGenerateController import generateMathQuestion
from app.utils.constants import SECTIONS
from app.utils.constants import SECTIONS_AND_TYPES
from typing import List


router = APIRouter()

def formatResponse(response: ServiceResponce):
    result = {
        "question": response.question,
        "correct_solution": response.correct_solution,
    }
    if response.other_solutions is not None:
        result["other_solutions"] = response.other_solutions
    if response.graph_img is not None:
        result["graph_img"] = response.graph_img
    return result
    


@router.post("/")
async def process_request(request: RequestModel):

    section = request.section
    type = request.question_type
   
    if section not in SECTIONS:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid section")
    if type not in SECTIONS_AND_TYPES[section]:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid type")
    response: List[ServiceResponce] = generateMathQuestion(request)
    
    res = list(map(formatResponse, response))


    return res
