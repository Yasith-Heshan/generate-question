from fastapi import FastAPI
from app.api.v1.question_controller import questionController
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
import os

APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(title="Simple FastAPI App")

print(f"Starting application in {APP_ENV} mode.")

@app.on_event("startup")
async def start_db():
    await init_db()
    print("MongoDB connection established.")


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

app.include_router(questionController, prefix="/api/v1")

# testing command
