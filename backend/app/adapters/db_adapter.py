from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List, Dict
from utils.constants import TableName
from dotenv import load_dotenv
import os

load_dotenv()


class MongoDBAdapter:
    _client: Optional[AsyncIOMotorClient] = None
    _db = None

    @classmethod
    def connect(cls):
        MONGO_URI = os.getenv("MONGO_URI")
        MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

        if not MONGO_URI or not MONGO_DB_NAME:
            raise ValueError("Missing MongoDB URI or DB name in environment variables.")

        cls._client = AsyncIOMotorClient(MONGO_URI)
        cls._db = cls._client[MONGO_DB_NAME]
        print("MongoDB connection established.")

    @classmethod
    def get_db(cls):
        if cls._db is None:
            raise ConnectionError("MongoDB not connected. Call connect() first.")
        return cls._db

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            print("MongoDB connection closed.")

    @classmethod
    async def insert_document(cls, collection_name: str, document: Dict[str, Any]) -> None:
        db = cls.get_db()
        await db[collection_name].insert_one(document)

    @classmethod
    async def find_one(cls, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db = cls.get_db()
        return await db[collection_name].find_one(query)

    @classmethod
    async def find_all(cls, collection_name: str, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        db = cls.get_db()
        cursor = db[collection_name].find(query)
        return await cursor.to_list(length=None)

    @classmethod
    async def add_question(cls, section: str, 
                           question_type: str, 
                           difficulty: int, 
                           question:str,
                           correctAnswer: str, 
                           mcqAnswers: Optional[List[str]] = []
                           
                           ) -> None:

        document = {
            "section": section,
            "questionType": question_type,
            "difficulty": difficulty,
            "question": question,
            "correctAnswer": correctAnswer,
            "mcqAnswers": mcqAnswers or []
        }
        try:
            await cls.insert_document("questions", document)
        except Exception as e:
            print(f"Error inserting question: {e}")
            raise e
        
    @classmethod
    async def add_all_questions(cls, questions: List[Dict[str, Any]]) -> None:
        if not questions:
            return
        
        try:
            await cls.get_db()["questions"].insert_many(questions)
        except Exception as e:
            print(f"Error inserting multiple questions: {e}")
            raise e
        
    @classmethod
    async def filter_questions(cls, section: Optional[str] = None, 
                               question_type: Optional[str] = None, 
                               difficulty: Optional[int] = None) -> List[Dict[str, Any]]:
        query = {}
        if section:
            query["section"] = section
        if question_type:
            query["questionType"] = question_type
        if difficulty is not None:
            query["difficulty"] = difficulty
        
        return await cls.find_all("questions", query)
    
    @classmethod
    async def get_all_sections(cls) -> List[str]:
        db = cls.get_db()
        sections = await db["questions"].distinct("section")
        return sections
    
    @classmethod
    async def get_all_question_types(cls) -> List[str]:
        db = cls.get_db()
        question_types = await db["questions"].distinct("questionType")
        return question_types
