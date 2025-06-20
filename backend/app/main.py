from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Simple FastAPI App")



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

app.include_router(api_router, prefix="/api/v1")
