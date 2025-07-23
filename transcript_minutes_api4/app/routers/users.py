from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User
from ..schemas.users import UserResponse, UserUpdate
from ..dependencies import get_current_active_user
from ..modules.auth import get_password_hash
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/users", tags=["ユーザー管理"])


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    logger.info(f"ユーザー情報取得: {current_user.username}")
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー情報更新開始: {current_user.username}")
    
    if user_update.username is not None:
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このユーザー名は既に使用されています"
            )
        current_user.username = user_update.username
    
    if user_update.email is not None:
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このメールアドレスは既に使用されています"
            )
        current_user.email = user_update.email
    
    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"ユーザー情報更新完了: {current_user.username}")
    return current_user


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"ユーザー一覧取得: {current_user.username}")
    users = db.query(User).offset(skip).limit(limit).all()
    return users
