from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import mathQuestionRequest

app = FastAPI()

origins = [
    os.getenv("FRONTEND_URL", "http://localhost:5173"),  # React dev server
]

print(f"Allowed CORS origins: {origins}")

# Add CORS middleware to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # allow specific origins
    allow_credentials=True,
    allow_methods=["*"],               # allow all methods (GET, POST, etc.)
    allow_headers=["*"],               # allow all headers
)

app.include_router(mathQuestionRequest.router, prefix="/api/math_question", tags=["math_question"])
