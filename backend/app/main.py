from fastapi import FastAPI
from app.api.v1.question_controller import questionController
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db



app = FastAPI(title="Simple FastAPI App")

@app.on_event("startup")
async def start_db():
    await init_db()
    print("MongoDB connection established.")


origins = [
    "http://localhost:5173",  # React dev server
]

# Add CORS middleware to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # allow specific origins
    allow_credentials=True,
    allow_methods=["*"],               # allow all methods (GET, POST, etc.)
    allow_headers=["*"],               # allow all headers
)

app.include_router(questionController, prefix="/api/v1")
