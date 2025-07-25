from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from src.schemas.auth import UserCreate, UserResponse, Token, LoginRequest, RefreshTokenRequest
from src.modules.auth import (
    authenticate_user, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    refresh_access_token,
    revoke_refresh_token,
    revoke_all_user_tokens
)
from src.modules.user_store import user_store
from src.dependencies.auth import get_current_active_user
from src.config import settings
import logging

router = APIRouter(prefix="/auth", tags=["authentication"])
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = user_store.get_user(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = user_store.create_user(user, hashed_password)
    
    logger.info(f"New user registered: {user.username}")
    
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(login_data: LoginRequest):
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(user.username, login_data.remember_me)
    
    logger.info(f"User logged in: {user.username}, remember_me: {login_data.remember_me}")
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshTokenRequest):
    token_data = refresh_access_token(refresh_data.refresh_token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    logger.info("Access token refreshed")
    
    return Token(**token_data)

@router.post("/logout")
async def logout(
    refresh_data: RefreshTokenRequest,
    current_user: UserResponse = Depends(get_current_active_user)
):
    revoke_refresh_token(refresh_data.refresh_token)
    logger.info(f"User logged out: {current_user.username}")
    return {"message": "Successfully logged out"}

@router.post("/logout-all")
async def logout_all_devices(current_user: UserResponse = Depends(get_current_active_user)):
    revoke_all_user_tokens(current_user.username)
    logger.info(f"All tokens revoked for user: {current_user.username}")
    return {"message": "Successfully logged out from all devices"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_active_user)):
    return current_user
