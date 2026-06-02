from beanie import Document
from typing import Optional

class UserModel(Document):
    username: str
    email: str
    hashed_password: str
    is_admin: bool = False
    requires_password_reset: bool = False

    class Settings:
        name = "users"
