from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import (
    create_user_model,
    authenticate_user,
    create_access_token,
    get_user_by_email,
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_create: UserCreate):
    existing = await get_user_by_email(user_create.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # Basic password rule
    if len(user_create.password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 6 characters")

    user = await create_user_model(user_create)
    return UserResponse(id=str(user.id), username=user.username, email=user.email)


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    user = await authenticate_user(user_login)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    from app.services.user_service import decode_access_token

    token_data = decode_access_token(token)
    if not token_data or not token_data.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user = await get_user_by_email(token_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(id=str(user.id), username=user.username, email=user.email)
