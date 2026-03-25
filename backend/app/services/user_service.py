import hashlib
import os
import time
from typing import Optional

from jose import JWTError, jwt

from app.core.config import settings
from app.models.user_model import UserModel
from app.schemas.user import UserCreate, UserLogin, TokenData


def hash_password(password: str, salt: Optional[bytes] = None) -> str:
    if salt is None:
        salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt.hex() + ":" + pwd_hash.hex()


def verify_password(password: str, hashed: str) -> bool:
    salt_hex, pwd_hash_hex = hashed.split(":")
    salt = bytes.fromhex(salt_hex)
    pwd_hash_check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return pwd_hash_check.hex() == pwd_hash_hex


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    to_encode = data.copy()
    now_seconds = int(time.time())
    expire = now_seconds + (expires_delta if expires_delta is not None else settings.JWT_EXPIRATION_MINUTES * 60)
    to_encode.update({"exp": expire, "iat": now_seconds})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            return None
        return TokenData(email=email)
    except JWTError:
        return None


async def get_user_by_email(email: str) -> Optional[UserModel]:
    return await UserModel.find_one(UserModel.email == email.lower())


async def create_user_model(user_create: UserCreate) -> UserModel:
    hashed_password = hash_password(user_create.password)
    user = UserModel(username=user_create.username, email=user_create.email.lower(), hashed_password=hashed_password)
    await user.insert()
    return user


async def authenticate_user(user_login: UserLogin) -> Optional[UserModel]:
    user = await get_user_by_email(user_login.email)
    if not user:
        return None
    if not verify_password(user_login.password, user.hashed_password):
        return None
    return user
