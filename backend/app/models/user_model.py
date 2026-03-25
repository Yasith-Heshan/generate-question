from beanie import Document
from typing import Optional

class UserModel(Document):
    username: str
    email: str
    hashed_password: str

    class Settings:
        name = "users"
