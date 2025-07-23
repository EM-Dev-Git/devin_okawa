from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User
from ..schemas.users import UserResponse, UserUpdate
from ..dependencies import get_current_user
from ..modules.auth import auth_service
from ..modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/users", tags=["ユーザー管理"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    logger.info(f"ユーザー情報取得: {current_user.username}")
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"ユーザー情報更新開始: {current_user.username}")
        
        if user_update.username and user_update.username != current_user.username:
            existing_user = db.query(User).filter(User.username == user_update.username).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="このユーザー名は既に使用されています"
                )
            current_user.username = user_update.username
        
        if user_update.email and user_update.email != current_user.email:
            existing_user = db.query(User).filter(User.email == user_update.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="このメールアドレスは既に使用されています"
                )
            current_user.email = user_update.email
        
        if user_update.password:
            current_user.hashed_password = auth_service.get_password_hash(user_update.password)
        
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"ユーザー情報更新成功: {current_user.username}")
        return current_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ユーザー情報更新エラー: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ユーザー情報の更新に失敗しました"
        )


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"全ユーザー一覧取得: {current_user.username}")
    users = db.query(User).all()
    return users
