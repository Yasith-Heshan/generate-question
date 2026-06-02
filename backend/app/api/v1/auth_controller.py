from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user_model import UserModel

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    PasswordResetRequest,
    UserListResponse,
)
from app.services.user_service import (
    create_user_model,
    create_admin_user,
    authenticate_user,
    create_access_token,
    get_user_by_email,
    get_all_users,
    reset_password_for_user,
    decode_access_token,
)
from typing import List

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    token_data = decode_access_token(token)
    if not token_data or not token_data.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = await get_user_by_email(token_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    user_create: UserCreate, current_user: UserModel = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create accounts",
        )

    existing = await get_user_by_email(user_create.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    if len(user_create.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters",
        )

    user = await create_user_model(user_create, requires_password_reset=True)
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
    )


@router.post(
    "/signup/admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup_admin(user_create: UserCreate):
    existing = await get_user_by_email(user_create.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    existing_admin = await UserModel.find_one(UserModel.is_admin == True)
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin account already exists"
        )

    admin_user = await create_admin_user(user_create)
    return UserResponse(
        id=str(admin_user.id),
        username=admin_user.username,
        email=admin_user.email,
        is_admin=True,
    )


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin):
    user = await authenticate_user(user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if user.requires_password_reset:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password reset required",
        )

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_admin=current_user.is_admin,
    )


@router.get("/users", response_model=List[UserListResponse])
async def get_users(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view user list",
        )

    users = await get_all_users()
    return [
        UserListResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
        )
        for user in users
    ]


@router.post("/reset-password")
async def reset_password(request: PasswordResetRequest):
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters",
        )

    user = await authenticate_user(
        UserLogin(email=request.email, password=request.old_password)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid current credentials",
        )

    if not user.requires_password_reset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset not required",
        )

    user = await reset_password_for_user(
        request.email, request.new_password, force_password_reset=False
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"message": "Password reset successful"}
